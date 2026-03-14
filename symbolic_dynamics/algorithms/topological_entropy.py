import numpy as np


def topological_entropy(matrix):

    eigvals = np.linalg.eigvals(matrix)

    spectral_radius = max(abs(eigvals))

    return np.log(spectral_radius)
