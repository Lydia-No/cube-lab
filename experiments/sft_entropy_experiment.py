from symbolic_dynamics.algorithms.sft_matrix import build_sft_matrix
from symbolic_dynamics.algorithms.topological_entropy import topological_entropy


alphabet = ["0", "1"]

forbidden = ["000"]


A, states = build_sft_matrix(alphabet, forbidden)

print("States:", states)

print("Adjacency matrix:")
print(A)

h = topological_entropy(A)

print("Topological entropy:", h)
