from cube_explorer.core import run_symbol_sequence
from cube_explorer.hypercube import Hypercube
from cube_explorer.grammars.sefer import apply_sefer_symbol

cube = Hypercube(8)

sequence = ["א","מ","ש"] * 10

path = run_symbol_sequence(
    0,
    sequence,
    apply_sefer_symbol,
    cube
)

print("Cube dimension:", cube.dimension)
print("Total states:", cube.states)
print("Path length:", len(path))
print("Unique states visited:", len(set(path)))
print("Path:", path)
