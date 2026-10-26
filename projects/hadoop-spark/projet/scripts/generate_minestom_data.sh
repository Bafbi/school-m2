#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/minestom-generator.env"

if [[ -f "$CONFIG_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
fi

MINESTOM_REPO_URL="${MINESTOM_REPO_URL:-https://github.com/Minestom/MinestomDataGenerator.git}"
MINESTOM_REF="${MINESTOM_REF:-2414f0d366aaacfa24e8fa91f17a94054e881607}"
MINESTOM_REPO_DIR="${MINESTOM_REPO_DIR:-$ROOT_DIR/.cache/MinestomDataGenerator}"
OUTPUT_DIR="${OUTPUT_DIR:-$ROOT_DIR/data/raw/minestom}"
ACCEPT_EULA="${ACCEPT_EULA:-true}"
MISE_JAVA_ALIAS="${MISE_JAVA_ALIAS:-generator}"

if ! command -v git >/dev/null 2>&1; then
  echo "git is required but was not found in PATH" >&2
  exit 1
fi

if ! command -v java >/dev/null 2>&1; then
  echo "java is required but was not found in PATH" >&2
  exit 1
fi

run_with_java() {
  if command -v mise >/dev/null 2>&1; then
    mise exec "java@${MISE_JAVA_ALIAS}" -- "$@"
  else
    "$@"
  fi
}

if [[ ! -d "$MINESTOM_REPO_DIR/.git" ]]; then
  mkdir -p "$(dirname "$MINESTOM_REPO_DIR")"
  git clone "$MINESTOM_REPO_URL" "$MINESTOM_REPO_DIR"
fi

git -C "$MINESTOM_REPO_DIR" fetch --all --tags --prune
git -C "$MINESTOM_REPO_DIR" checkout "$MINESTOM_REF"

if [[ "$ACCEPT_EULA" != "true" ]]; then
  echo "EULA acceptance is required to run generation. Set ACCEPT_EULA=true in minestom-generator.env." >&2
  exit 1
fi

JAVA_VERSION="$(run_with_java java -version 2>&1 | head -n1 | sed 's/"//g')"

(
  cd "$MINESTOM_REPO_DIR"
  run_with_java ./gradlew --no-daemon generateData -Peula=true
)

SOURCE_DIR="$MINESTOM_REPO_DIR/src/main/resources"
if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Generation succeeded but source output directory was not found: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
rsync -a --delete "$SOURCE_DIR/" "$OUTPUT_DIR/"

PINNED_COMMIT="$(git -C "$MINESTOM_REPO_DIR" rev-parse HEAD)"
GENERATED_AT_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

cat > "$OUTPUT_DIR/_manifest.json" <<EOF
{
  "source_repository": "$MINESTOM_REPO_URL",
  "source_ref_requested": "$MINESTOM_REF",
  "source_commit_resolved": "$PINNED_COMMIT",
  "generated_at_utc": "$GENERATED_AT_UTC",
  "java_version": "$JAVA_VERSION",
  "generator_output_source": "src/main/resources",
  "eula_accepted": true
}
EOF

echo "Minestom data generated in: $OUTPUT_DIR"
echo "Manifest written to: $OUTPUT_DIR/_manifest.json"
