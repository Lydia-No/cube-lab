import plotly.graph_objects as go
from cube_explorer.hypercube import Hypercube
from cube_explorer.analysis import entropy


def entropy_scan(dimensions, steps=20000):

    results = {}

    for d in dimensions:

        cube = Hypercube(d)
        seq = cube.random_walk(steps)

        H = entropy(seq)

        results[d] = H

        print(f"Q{d} entropy: {H:.3f}")

    return results


def plot_entropy(results):

    dims = list(results.keys())
    ent = list(results.values())

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[f"Q{d}" for d in dims],
            y=ent
        )
    )

    fig.update_layout(
        title="Hypercube Entropy Growth",
        xaxis_title="Dimension",
        yaxis_title="Entropy (bits)"
    )

    fig.show()


if __name__ == "__main__":

    dims = range(3, 9)

    results = entropy_scan(dims)

    plot_entropy(results)
