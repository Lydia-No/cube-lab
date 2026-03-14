from cube_explorer.core import run_symbol_sequence
from cube_explorer.grammars.sefer import apply_sefer_symbol

sequence = ["א","מ","ש"] * 10

path = run_symbol_sequence(0, sequence, apply_sefer_symbol)

print("Sequence length:", len(sequence))
print("Path:", path)
print("Unique states:", len(set(path)))
