from cube_explorer.grammars import get_grammar
from cube_explorer.core import CubeGraph, SymbolicWalker

def main() -> None:
    g = get_grammar("runes")
    cube = CubeGraph()
    w = SymbolicWalker(cube=cube, grammar=g)

    concept = "collective intelligence"
    symbols = ["ᚠ", "ᚢ", "ᚦ", "ᚠ", "ᚢ", "ᚦ"]

    start, path, seq, score = w.run_concept(concept, symbols=symbols)
    print("Grammar:", g.metadata().display_name)
    print("Start:", start)
    print("Path:", path)
    print("Sequence:", " ".join(seq))
    print("Score:", score)

if __name__ == "__main__":
    main()
