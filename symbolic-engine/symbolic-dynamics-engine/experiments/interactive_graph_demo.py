from symbolic_dynamics.algorithms.pipeline import SFTPipeline
from symbolic_dynamics.visualization.interactive_graph import interactive_graph


pipe = SFTPipeline(["0","1"],["000"])

G,_ = pipe.build_graph()

interactive_graph(G)
