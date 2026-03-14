import numpy as np
import matplotlib.pyplot as plt
from symbolic_dynamics.algorithms.pipeline import SFTPipeline


alphabet = ["0","1"]

forbidden_patterns = [["000"],["111"],["000","111"]]

values = []

for f in forbidden_patterns:

    pipe = SFTPipeline(alphabet,f)

    values.append(pipe.entropy())

plt.bar(range(len(values)),values)

plt.title("entropy comparison")

plt.show()
