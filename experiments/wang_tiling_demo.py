from symbolic_dynamics.geometry.lattice.wang_tile import WangTile
from symbolic_dynamics.geometry.lattice.wang_solver import WangSolver
from symbolic_dynamics.visualization.wang_plot import show_tiling


tiles = [

    WangTile(0,0,0,0,"A"),
    WangTile(0,1,0,1,"B"),
    WangTile(1,0,1,0,"C"),
    WangTile(1,1,1,1,"D")

]


solver = WangSolver(tiles,6)

if solver.solve():

    print("tiling found")

    show_tiling(solver.grid)

else:

    print("no tiling")
