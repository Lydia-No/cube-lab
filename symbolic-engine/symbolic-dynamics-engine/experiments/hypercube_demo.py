from symbolic_dynamics.geometry.hypercube.hypercube_shift import HypercubeShift


cube = HypercubeShift(["0","1"],4,3)

cube.show()

cube.shift(2)

print("after shift")

cube.show()
