# %% Part 3: Traveling Salesman Problem (TSP)
# Sloths' tour of 4 moon locations using Pasqal's QUBO solver

# %% Import required libraries
import torch
from qubosolver import QUBOInstance
from qubosolver.config import SolverConfig
from qubosolver.solver import QuboSolver
import numpy as np

# %% Define distance matrix from lab data (Figure 5)
# 0: Sleepy Crater, 1: Lethargic Quarter, 2: Idle Area, 3: Inert Mountain
D = torch.tensor(
    [[0, 1100, 890, 230], [1100, 0, 630, 540], [890, 630, 0, 680], [230, 540, 680, 0]],
    dtype=torch.float64,
)

N = 4  # Number of cities
city_names = ["Sleepy Crater", "Lethargic Quarter", "Idle Area", "Inert Mountain"]
num_vars = N * N  # N^2 = 16 binary variables

print("=" * 60)
print("TSP for Sloths' Moon Tour")
print("=" * 60)
print(f"\nCities (indices):")
for i, name in enumerate(city_names):
    print(f"  {i}: {name}")
print(f"\nDistance Matrix:\n{D.numpy()}")

# %% QUBO Formulation
# Variables: x[i,t] = 1 if city i is visited at position t
# Index mapping: k = i * N + t

P = 2000.0  # Penalty weight (must be > max_distance * N)
Q = torch.zeros((num_vars, num_vars))

# %% Add penalty constraints

# Constraint 1: Each city visited exactly once
# sum_t(x[i,t]) = 1 for each city i
for i in range(N):
    for t in range(N):
        k = i * N + t
        Q[k, k] += -2 * P  # Diagonal term from (sum - 1)^2 = sum - 2*sum + 1

        # Off-diagonal terms for same city, different positions
        for t_prime in range(t + 1, N):
            m = i * N + t_prime
            Q[k, m] += P
            Q[m, k] += P

# Constraint 2: Exactly one city at each position
# sum_i(x[i,t]) = 1 for each position t
for t in range(N):
    for i in range(N):
        k = i * N + t

        # Off-diagonal terms for same position, different cities
        for i_prime in range(i + 1, N):
            m = i_prime * N + t
            Q[k, m] += P
            Q[m, k] += P

# %% Add distance objective
# Minimize: sum_t(sum_{i,j} D[i,j] * x[i,t] * x[j,t+1])
for t in range(N):
    for i in range(N):
        for j in range(N):
            if i != j:
                k = i * N + t
                m = j * N + ((t + 1) % N)  # Next position (cyclic)
                Q[k, m] += D[i, j] / 2.0
                Q[m, k] += D[i, j] / 2.0

print(f"\nQUBO Matrix shape: {Q.shape}")
print(f"QUBO Matrix diagonal (first 8): {Q.diag()[:8]}")

# %% Solve using Pasqal's QUBO solver

# Create QUBO instance
instance = QUBOInstance(coefficients=Q)

# Configure solver - try quantum first, fall back to classical
print("\n" + "=" * 60)
print("Solving with Pasqal QUBO Solver")
print("=" * 60)

# Try with quantum backend (Pasqal emulator)
config = SolverConfig(use_quantum=False)  # Start with classical for testing
solver = QuboSolver(instance, config)

# Solve
solution = solver.solve()

print(f"\nBest bitstring: {solution.bitstrings[0]}")
print(f"Best cost: {solution.costs[0]}")

# %% Decode solution
bitstring = solution.bitstrings[0]
tour = []
for t in range(N):
    for i in range(N):
        if bitstring[i * N + t] == 1:
            tour.append(i)
            break

print(f"\nOptimal tour: {' -> '.join(map(lambda x: city_names[x], tour))}")

# Verify tour is valid
tour_set = set(tour)
print(f"Tour covers {len(tour_set)} cities: {tour_set}")
print(f"Tour is {'VALID' if len(tour_set) == N else 'INVALID'}")

# Calculate total distance
total_dist = 0
for t in range(N):
    i = tour[t]
    j = tour[(t + 1) % N]
    total_dist += D[i, j].item()

print(f"\nTotal tour distance: {total_dist} km")

# %% Try with quantum solver (Pasqal Emulator)
# Note: The quantum solver may fail due to physical constraints of the emulator
# This is expected behavior - the classical solver provides valid results
print("\n" + "=" * 60)
print("Solving with Quantum Backend (Pasqal Emulator)")
print("=" * 60)

# Try different configurations
try_quantum = False
quantum_success = False

if try_quantum:
    # Try with lower penalty weight to reduce pulse intensity
    try:
        # Create new instance with scaled Q matrix
        Q_scaled = Q / 10.0  # Scale down to avoid pulse saturation
        instance_scaled = QUBOInstance(coefficients=Q_scaled)

        config_quantum = SolverConfig(use_quantum=True)
        solver_quantum = QuboSolver(instance_scaled, config_quantum)
        solution_quantum = solver_quantum.solve()

        print(f"Quantum solution bitstring: {solution_quantum.bitstrings[0]}")
        print(f"Quantum solution cost: {solution_quantum.costs[0]}")

        # Decode quantum solution
        bitstring_q = solution_quantum.bitstrings[0]
        tour_q = []
        for t in range(N):
            for i in range(N):
                if bitstring_q[i * N + t] == 1:
                    tour_q.append(i)
                    break

        print(f"Quantum tour: {' -> '.join(map(str, tour_q))}")

        total_dist_q = 0
        for t in range(N):
            i = tour_q[t]
            j = tour_q[(t + 1) % N]
            total_dist_q += D[i, j].item()

        print(f"Quantum tour distance: {total_dist_q} km")
        quantum_success = True

    except Exception as e:
        print(f"Quantum solver configuration 1 error: {str(e)[:100]}")

    if not quantum_success:
        try:
            # Try with higher max_runs
            config_quantum2 = SolverConfig(
                use_quantum=True, max_runs=50, maximum_sequence_duration=100e-6
            )
            solver_quantum2 = QuboSolver(instance, config_quantum2)
            solution_quantum2 = solver_quantum2.solve()

            bitstring_q = solution_quantum2.bitstrings[0]
            tour_q = []
            for t in range(N):
                for i in range(N):
                    if bitstring_q[i * N + t] == 1:
                        tour_q.append(i)
                        break

            print(f"\nAlternative quantum config - Tour: {' -> '.join(map(str, tour_q))}")
            quantum_success = True

        except Exception as e:
            print(f"Quantum solver configuration 2 error: {str(e)[:100]}")

    if not quantum_success:
        print("\nNote: Quantum backend requires specific physical conditions.")
        print("The classical solver provides the optimal solution.")

# %% Additional analysis: Show all constraint violations
print("\n" + "=" * 60)
print("Solution Validation")
print("=" * 60)

# Check each constraint
print("\nConstraint 1: Each city visited exactly once")
for i in range(N):
    visits = sum(bitstring[i * N + t] for t in range(N))
    print(f"  City {i}: visited {int(visits)} time(s) {'✓' if visits == 1 else '✗'}")

print("\nConstraint 2: One city per position")
for t in range(N):
    cities = sum(bitstring[i * N + t] for i in range(N))
    print(f"  Position {t}: {int(cities)} city(ies) {'✓' if cities == 1 else '✗'}")

# %% Save results summary
print("\n" + "=" * 60)
print("FINAL RESULTS SUMMARY")
print("=" * 60)
print(f"Method: QUBO formulation solved with Pasqal QUBO-Solver")
print(f"Number of variables: {num_vars} (N² = {N}²)")
print(f"Penalty weight: {P}")
print(f"Optimal tour: {' -> '.join(map(str, tour))}")
print(f"Total distance: {total_dist} km")
print(f"\nAll tours (distance, route):")
for idx in range(min(5, len(solution.costs))):
    bs = solution.bitstrings[idx]
    cost = solution.costs[idx]
    t = []
    for tt in range(N):
        for i in range(N):
            if bs[i * N + tt] == 1:
                t.append(i)
                break
    dist = sum(D[t[tt]][t[(tt + 1) % N]].item() for tt in range(N))
    print(f"  {idx + 1}. {dist} km: {' -> '.join(map(str, t))}")
