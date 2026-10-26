# quantum — quantum computing labs

Two lab sessions from the quantum computing course.

- `lab/` — simulated annealing on DWave/Pasqal hardware for a TSP: instance
  generation (`tsp_file_generation.py`), the solver runs (`part3.py`,
  `part3_reel.py`), the lab assignment (`DWave_…_Sloths.pdf`, with its text as
  `.md`) and the report written for it
  (`Quantum_Annealing_DWave_Lab_Report.pdf`, team Cacheux / Pousset / Kelma /
  Eudeline).
- `grover_lab/` — Grover's algorithm on Qiskit, in three versions: the solo run,
  the `_V1`, and the version the group handed in; plus the circuits as rendered
  images (`circuit.png`, `grover.png`).

Lecture material lives in `cours/` (course slides) and `lab/` (the DWave/Pasqal lab
assignment, whose text is also alongside as `.md`). PDFs were recompressed with
Ghostscript at `/printer` quality. The environment is declared in `mise.toml` /
`pyproject.toml` / `uv.lock`.
