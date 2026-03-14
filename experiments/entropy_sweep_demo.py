from symbolic_dynamics.algorithms.entropy.entropy_experiment import entropy_sweep


alphabet = ["0","1"]

forbidden_sets = [
    ["000"],
    ["111"],
    ["000","111"]
]

results = entropy_sweep(alphabet, forbidden_sets)

for f,h in results:
    print("forbidden:", f, "entropy:", h)
