from cube_explorer.core import run_symbol_sequence
from cube_explorer.visualization import plot_cube_walk
from cube_explorer.grammars.sefer import apply_sefer_symbol

path = run_symbol_sequence(0, ["א","מ","ש","א"], apply_sefer_symbol)

print("Path:", path)

fig = plot_cube_walk(path)
fig.show()

