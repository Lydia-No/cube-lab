from cube_explorer.core import CubeGraph, SymbolicWalker
from cube_explorer.visualization import plot_cube_walk

def main() -> None:
    cube = CubeGraph()
    walker = SymbolicWalker(cube)

    start, path, seq, score = walker.run_concept("collective intelligence")

    print("Start:", start)
    print("Path:", path)
    print("Sequence:", " → ".join(seq))
    print("Score:", score)

    fig = plot_cube_walk(path)
    fig.show()

if __name__ == "__main__":
    main()
