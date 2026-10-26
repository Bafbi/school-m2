# school-m2 — M2 coursework (2025/2026)

One repository per school year. This one holds the 2025/2026 (M2) work at
ISEN/Junia: projects, reports and labs.

Course handouts are kept, per project (`class/`, `cours/`), compressed with
Ghostscript at `/printer` quality — same page count, 50–90% smaller. Generated
data, credentials and build output are not committed.

## Projects

| Project | What it is | Course |
|---|---|---|
| [hadoop-spark](projects/hadoop-spark) | Minecraft item-complexity analysis: Minestom data generation → curated parquet → PySpark | Big Data |
| [spark-project](projects/spark-project) | Colab version of the same Spark project (as submitted) | Big Data |
| [quantum](projects/quantum) | DWave/Pasqal simulated-annealing lab (TSP) + Grover on Qiskit | Quantum computing |
| [veille-tech](projects/veille-tech) | Typst report on air-gapped Kubernetes, CASD and DevSecOps | Veille & prospective technologiques |
| [locchain](projects/locchain) | Poster + infographic on French public digital infrastructure and sovereign cloud | — |
| [mlops](projects/mlops) | Streamlit chatbot skeleton; the project was never finished | MLOps |
| [greenit-report](projects/greenit-report) | Group report and presentation | GreenIT / numérique responsable |

## Kept outside this repo

These already live in their own repositories and are not duplicated here:

- [`Bafbi/school-m2-biostats`](https://github.com/Bafbi/school-m2-biostats) — biostatistics
- [`Bafbi/school-m2-cloud`](https://github.com/Bafbi/school-m2-cloud) — cloud computing
- [`Summers-Team/school-m2-bi-project`](https://github.com/Summers-Team/school-m2-bi-project) — team BI project
- [`CASD-EU/kube`](https://github.com/CASD-EU/kube) — reference repository used while writing the veille report

## Notes

- Datasets are generated, not versioned: `hadoop-spark/projet/data/curated` holds
  the analysis-ready parquet tables, while the raw Minestom JSON is rebuilt with
  the scripts in `projet/scripts/`. Credentials for that pipeline (`kaggle.json`)
  are excluded on purpose.
- PDFs in this repository are the originals run through
  `gs -dPDFSETTINGS=/printer` (`~/prep/scripts/compress_pdfs.py`); page counts and
  layout are unchanged.
- Earlier years live in their own repositories (`school-m1-*`, `cir2-*`) and in
  `summer-*` for the ISEN 3 final-year project.
