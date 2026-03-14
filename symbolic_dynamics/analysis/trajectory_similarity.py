import numpy as np


def trajectory_distance(traj_a, traj_b):
    """
    Euclidean distance between two trajectories.
    """

    if len(traj_a) != len(traj_b):
        raise ValueError("Trajectories must have same length")

    dist = 0.0

    for a, b in zip(traj_a, traj_b):

        diff = np.array(a) - np.array(b)

        dist += np.linalg.norm(diff)

    return dist


def trajectory_matrix(trajectories):
    """
    Compute pairwise trajectory distance matrix.
    """

    n = len(trajectories)

    M = np.zeros((n, n))

    for i in range(n):
        for j in range(n):

            M[i, j] = trajectory_distance(
                trajectories[i],
                trajectories[j]
            )

    return M
