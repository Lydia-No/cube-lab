from cube_explorer.core import run_symbol_sequence
from cube_explorer.grammars.enochian import apply_enochian_symbol

start_state = 0
sequence = ["Pa", "Veh", "Ged", "Pa"]

path = run_symbol_sequence(start_state, sequence, apply_enochian_symbol)

print("Grammar: Enochian")
print("Sequence:", sequence)
print("Path:", path)
