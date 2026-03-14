import numpy as np
from symbolic_dynamics.algorithms.pipeline import SFTPipeline


def entropy_sweep(alphabet, forbidden_sets):

    results = []

    for f in forbidden_sets:

        pipe = SFTPipeline(alphabet, f)

        h = pipe.entropy()

        results.append((f, h))

    return results
