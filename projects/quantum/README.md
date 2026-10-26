# quantum — quantum computing labs

Two lab sessions from the quantum computing course.

- `lab/` — simulated annealing on DWave/Pasqal hardware for a TSP: instance
  generation (`tsp_file_generation.py`), the solver runs (`part3.py`,
  `part3_reel.py`) and the write-up (`lab.typ`, plus its text as `.md`).
- `grover_lab/` — Grover's algorithm on Qiskit, with the circuits as rendered
  images (`circuit.png`, `grover.png`).

Lecture material lives in `cours/` (course slides) and `lab/` (the DWave/Pasqal lab
assignment, whose text is also alongside as `.md`). PDFs were recompressed with
Ghostscript at `/printer` quality. The environment is declared in `mise.toml` /
`pyproject.toml` / `uv.lock`.
