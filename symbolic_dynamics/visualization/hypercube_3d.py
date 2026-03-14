import itertools
import networkx as nx
import matplotlib.pyplot as plt


def draw_hypercube_trajectory(trajectory, dimension=3):

    nodes = list(itertools.product([0,1], repeat=dimension))

    G = nx.Graph()

    for n in nodes:
        G.add_node(n)

    for n in nodes:

        for i in range(dimension):

            neighbor = list(n)

            neighbor[i] ^= 1

            neighbor = tuple(neighbor)

            G.add_edge(n, neighbor)

    pos = nx.spring_layout(G, dim=3)

    fig = plt.figure()

    ax = fig.add_subplot(projection='3d')

    for edge in G.edges():

        x = [pos[edge[0]][0], pos[edge[1]][0]]
        y = [pos[edge[0]][1], pos[edge[1]][1]]
        z = [pos[edge[0]][2], pos[edge[1]][2]]

        ax.plot(x,y,z,color="gray",alpha=0.3)

    traj_points = [pos.get(tuple(state[:dimension]), None) for state in trajectory]

    traj_points = [p for p in traj_points if p]

    xs = [p[0] for p in traj_points]
    ys = [p[1] for p in traj_points]
    zs = [p[2] for p in traj_points]

    ax.plot(xs,ys,zs,color="red",marker="o")

    plt.title("Hypercube trajectory")

    plt.show()
