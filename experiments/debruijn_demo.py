from symbolic_dynamics.algorithms.debruijn import debruijn_graph
from symbolic_dynamics.visualization.shift_graph import draw_graph


alphabet = ["0","1"]

G = debruijn_graph(alphabet,3)

draw_graph(G)
