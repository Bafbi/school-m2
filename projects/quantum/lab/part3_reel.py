import torch
from qubosolver import QUBOInstance
from qubosolver.config import ClassicalConfig, SolverConfig
from qubosolver.solver import QuboSolverClassical, QuboSolverQuantum

# define QUBO
Q = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
instance = QUBOInstance(coefficients=Q)

# Create a SolverConfig object with classical solver options.
classical_config = ClassicalConfig(
    classical_solver_type="cplex",
    cplex_maxtime=10.0,
    cplex_log_path="test_solver.log",
)
config = SolverConfig(use_quantum=False, classical=classical_config)

# Instantiate the classical solver via the pipeline's classical solver dispatcher.
classical_solver = QuboSolver(instance, config)

# Solve the QUBO problem.
solution = classical_solver.solve()
print(solution)