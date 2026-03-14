from symbolic_dynamics.geometry.lattice.z2_shift import Z2Shift
from symbolic_dynamics.visualization.lattice_plot import show_lattice


system = Z2Shift(["0","1"],20)

show_lattice(system.state)

system.shift_x()

show_lattice(system.state)
