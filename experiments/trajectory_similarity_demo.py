from symbolic_dynamics.analysis.trajectory_similarity import trajectory_matrix


trajectories = [

    [(0,0,0),(1,0,0),(1,1,0)],
    [(0,0,0),(0,1,0),(0,1,1)],
    [(0,0,0),(1,0,0),(1,0,1)]

]

M = trajectory_matrix(trajectories)

print("Distance matrix:")

print(M)
