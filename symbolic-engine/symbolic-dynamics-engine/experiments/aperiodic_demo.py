from symbolic_dynamics.geometry.lattice.aperiodic_tiling import AperiodicTile, AperiodicTilingSystem


tiles = [

    AperiodicTile(0,1,0,1,"A"),
    AperiodicTile(1,0,1,0,"B"),
    AperiodicTile(1,1,0,0,"C"),
    AperiodicTile(0,0,1,1,"D")

]


system = AperiodicTilingSystem(tiles,6)

if system.solve():
    print("aperiodic tiling found")

else:
    print("no tiling")
