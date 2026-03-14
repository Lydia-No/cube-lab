import matplotlib.pyplot as plt


def show_lattice(grid):

    plt.imshow(grid, cmap="binary")

    plt.title("symbolic configuration")

    plt.show()
