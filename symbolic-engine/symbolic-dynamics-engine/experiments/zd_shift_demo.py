from symbolic_dynamics.geometry.lattice.zd_shift import ZdShift


system = ZdShift(["0","1"],3,5)

system.show()

system.shift(1)

print("after shift")

system.show()
