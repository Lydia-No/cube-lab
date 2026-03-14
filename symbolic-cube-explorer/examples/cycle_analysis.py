from cube_explorer.core import run_symbol_sequence
from cube_explorer.grammars.sefer import apply_sefer_symbol

def find_cycle(path):
    visited = {}

    for i, state in enumerate(path):
        if state in visited:
            start = visited[state]
            cycle = path[start:i]
            return cycle
        visited[state] = i

    return None


start_state = 0
sequence = ["א", "מ", "ש", "א", "מ", "ש", "א"]

path = run_symbol_sequence(start_state, sequence, apply_sefer_symbol)

print("Sequence:", sequence)
print("Path:", path)

cycle = find_cycle(path)

if cycle:
    print("Cycle detected:", cycle)
else:
    print("No cycle detected")

