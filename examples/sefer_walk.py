from cube_explorer.core import run_symbol_sequence
from cube_explorer.grammars.sefer import apply_sefer_symbol

start_state = 0
sequence = ["א", "מ", "ש", "א"]

path = run_symbol_sequence(start_state, sequence, apply_sefer_symbol)

print("Grammar: Sefer")
print("Sequence:", sequence)
print("Path:", path)
