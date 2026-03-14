from symbolic_dynamics.visualization.hypercube_plot import build_hypercube_graph, plot_trajectory

G = build_hypercube_graph(3)

trajectory = [
(0,0,0),
(1,0,0),
(1,1,0),
(0,1,0),
(0,1,1)
]

plot_trajectory(G, trajectory)
