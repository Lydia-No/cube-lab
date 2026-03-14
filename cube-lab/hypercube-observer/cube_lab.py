import argparse
import random
import math
from collections import defaultdict

import plotly.graph_objects as go

from cube_explorer.hypercube import Hypercube


def vertex_to_point(vertex, dim):
    bits = format(vertex, f"0{dim}b")
    return [1 if b == "1" else -1 for b in bits]


def project_4d_to_3d(p):
    x, y, z, w = p
    scale = 1 / (2 - w)
    return (x * scale, y * scale, z * scale)


def to_sky(p):
    x, y, z = p
    r = math.sqrt(x*x + y*y + z*z)
    az = math.degrees(math.atan2(y, x))
    el = math.degrees(math.asin(z / r))
    return az, el


def run_cube():

    cube = Hypercube(3)

    seq, vertices = cube.random_walk(60, return_vertices=True)

    points = [vertex_to_point(v,3) for v in vertices]

    xs=[p[0] for p in points]
    ys=[p[1] for p in points]
    zs=[p[2] for p in points]

    fig=go.Figure()

    fig.add_trace(go.Scatter3d(
        x=xs,y=ys,z=zs,
        mode="markers+lines",
        marker=dict(size=6),
        line=dict(width=4)
    ))

    fig.update_layout(title="Cube Walk")

    fig.show()


def run_tesseract():

    cube = Hypercube(4)

    seq, vertices = cube.random_walk(60, return_vertices=True)

    points4=[vertex_to_point(v,4) for v in vertices]

    points3=[project_4d_to_3d(p) for p in points4]

    xs=[p[0] for p in points3]
    ys=[p[1] for p in points3]
    zs=[p[2] for p in points3]

    fig=go.Figure()

    fig.add_trace(go.Scatter3d(
        x=xs,y=ys,z=zs,
        mode="markers+lines",
        marker=dict(size=6,color="orange"),
        line=dict(width=4,color="red")
    ))

    fig.update_layout(title="Tesseract Walk")

    fig.show()


def run_sky():

    cube = Hypercube(4)

    seq, vertices = cube.random_walk(80, return_vertices=True)

    stars=[]
    transitions=defaultdict(int)

    prev=None

    for v in vertices:

        p4=vertex_to_point(v,4)
        p3=project_4d_to_3d(p4)

        stars.append(p3)

        if prev is not None:
            transitions[(prev,p3)] += 1

        prev=p3

    star_x=[]
    star_y=[]

    for p in stars:

        az,el=to_sky(p)

        star_x.append(az)
        star_y.append(el)

    fig=go.Figure()

    fig.add_trace(go.Scatter(
        x=star_x,
        y=star_y,
        mode="markers"
    ))

    fig.update_layout(
        title="Symbolic Sky",
        xaxis_title="Azimuth",
        yaxis_title="Elevation"
    )

    fig.show()


def run_motifs():

    cube = Hypercube(4)

    seq, vertices = cube.random_walk(200, return_vertices=True)

    cycles=defaultdict(int)

    for i in range(len(seq)-4):

        c=tuple(seq[i:i+4])

        cycles[c]+=1

    result=sorted(cycles.items(),key=lambda x:-x[1])

    print("\nTop symbolic motifs:\n")

    for c,count in result[:10]:

        print("".join(c)," count=",count)


def run_learning():

    dim=4
    steps=200

    cube=Hypercube(dim)

    vertex=random.randrange(1<<dim)

    transitions=defaultdict(int)

    seq=[]

    for _ in range(steps):

        candidates=[]

        for d in range(dim):

            nv=vertex^(1<<d)

            candidates.append((d,nv))

        weights=[]

        for d,nv in candidates:

            w=transitions[(vertex,nv)]+1

            weights.append(w)

        d,nv=random.choices(candidates,weights=weights)[0]

        seq.append(cube.symbols[d])

        transitions[(vertex,nv)]+=1

        vertex=nv

    print("\nLearning sequence:\n")

    print(" ".join(seq[:50]))


def main():

    parser=argparse.ArgumentParser()

    parser.add_argument("mode")

    args=parser.parse_args()

    if args.mode=="cube":
        run_cube()

    elif args.mode=="tesseract":
        run_tesseract()

    elif args.mode=="sky":
        run_sky()

    elif args.mode=="motifs":
        run_motifs()

    elif args.mode=="learn":
        run_learning()

    else:
        print("Modes: cube | tesseract | sky | motifs | learn")


if __name__=="__main__":
    main()
