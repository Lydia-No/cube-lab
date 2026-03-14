import matplotlib.pyplot as plt
import numpy as np


def show_tiling(grid):

    size = grid.shape[0]

    image = np.zeros((size, size))

    for i in range(size):

        for j in range(size):

            tile = grid[i][j]

            if tile:
                image[i][j] = hash(tile.name) % 10

    plt.imshow(image)

    plt.title("Wang Tiling")

    plt.show()
