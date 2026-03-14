from symbolic_dynamics.geometry.cube.cube_shift import CubeShift


cube = CubeShift(["0","1"],4)

cube.show()

cube.shift_x()

print("after shift x")

cube.show()
