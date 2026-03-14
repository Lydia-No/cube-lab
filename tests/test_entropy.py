from symbolic_dynamics.algorithms.sft_matrix import build_sft_matrix
from symbolic_dynamics.algorithms.topological_entropy import topological_entropy


def test_entropy():

    alphabet = ["0","1"]

    forbidden = ["000"]

    A,_ = build_sft_matrix(alphabet,forbidden)

    h = topological_entropy(A)

    assert h > 0
