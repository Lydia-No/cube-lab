import matplotlib.pyplot as plt


def plot_trajectory(trajectory, save_path="trajectory.png"):

    xs = [p[0] for p in trajectory]
    ys = [p[1] for p in trajectory]

    plt.figure()

    plt.plot(xs, ys, marker="o")

    plt.title("Symbolic Trajectory")

    plt.xlabel("Axis 0")
    plt.ylabel("Axis 1")

    plt.grid(True)

    plt.savefig(save_path)

    print(f"Trajectory plot saved to {save_path}")
