import numpy as np
from sklearn.cluster import KMeans


def flatten_trajectory(trajectory):
    """
    Convert trajectory of states into a flat vector.
    """

    flat = []

    for state in trajectory:
        flat.extend(state)

    return flat


def cluster_trajectories(trajectories, k=3):
    """
    Cluster trajectories based on their state sequences.
    """

    vectors = []

    for traj in trajectories:
        vectors.append(flatten_trajectory(traj))

    X = np.array(vectors)

    model = KMeans(n_clusters=k, random_state=0)

    labels = model.fit_predict(X)

    return labels
