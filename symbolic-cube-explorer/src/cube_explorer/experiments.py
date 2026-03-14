from cube_explorer.hypercube import Hypercube
from cube_explorer.analysis import entropy


def entropy_curve(start=3, end=12, steps=20000, plot=True):

    dims = []
    entropies = []

    print("\nEntropy vs Hypercube Dimension\n")

    for d in range(start, end + 1):

        cube = Hypercube(d)

        seq = cube.random_walk(steps)

        H = entropy(seq)

        dims.append(d)
        entropies.append(H)

        print(f"Q{d}: entropy = {H:.5f}")

    if plot:

        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=dims,
                y=entropies,
                mode="lines+markers",
                name="entropy"
            )
        )

        fig.update_layout(
            title="Entropy Growth on Hypercube Walks",
            xaxis_title="Dimension (Qn)",
            yaxis_title="Entropy"
        )

        fig.show()

    return dims, entropies
