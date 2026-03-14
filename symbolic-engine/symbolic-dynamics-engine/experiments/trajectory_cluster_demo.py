from symbolic_dynamics.analysis.trajectory_clustering import cluster_trajectories

trajectories = [

    [(0,0,0),(1,0,0),(1,1,0)],
    [(0,0,0),(0,1,0),(0,1,1)],
    [(0,0,0),(1,0,0),(1,0,1)],
    [(0,0,0),(0,1,0),(1,1,0)]

]

labels = cluster_trajectories(trajectories, k=2)

print("Cluster labels:")
print(labels)
