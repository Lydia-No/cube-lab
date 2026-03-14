from cube_explorer.core import run_symbol_sequence
from cube_explorer.grammars.runes import apply_rune_symbol

start_state = 0
sequence = ["ᚠ", "ᚢ", "ᚦ", "ᚠ"]

path = run_symbol_sequence(start_state, sequence, apply_rune_symbol)

print("Grammar: Runes")
print("Sequence:", sequence)
print("Path:", path)
