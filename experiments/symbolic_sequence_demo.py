from symbolic_dynamics.state_spaces.kcube import KCube
from symbolic_dynamics.walkers.symbolic_walker import SymbolicWalker
from symbolic_dynamics.visualization.trajectory_plot import plot_trajectory

cube = KCube(3,4)

grammar = {
    "cave": (1,0,0),
    "horse": (0,1,0),
    "storm": (0,0,1),
    "ladder": (1,1,0)
}

sequence = ["cave","horse","cave","storm","ladder"]

walker = SymbolicWalker(cube, grammar)

trajectory = walker.run(sequence)

print(trajectory)

plot_trajectory(trajectory)
