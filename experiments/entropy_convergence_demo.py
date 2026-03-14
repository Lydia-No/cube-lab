import math
import matplotlib.pyplot as plt

from symbolic_dynamics.core.examples import golden_mean_shift


system = golden_mean_shift()

ns = []
values = []

for n in range(1, 12):

    count = system.word_growth(n)

    estimate = math.log(count) / n

    ns.append(n)
    values.append(estimate)

    print(f"n={n} words={count} estimate={estimate}")


plt.plot(ns, values, marker="o")

plt.xlabel("n (word length)")
plt.ylabel("log(|L_n|) / n")

plt.title("Entropy convergence")

plt.grid(True)

plt.savefig("docs/entropy_convergence.png")
print("Saved plot to docs/entropy_convergence.png")
