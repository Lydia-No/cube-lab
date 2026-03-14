from cube_explorer.core import CubeGraph, SymbolicWalker

concepts=[
"collective intelligence",
"symbolic AI",
"graph theory",
"creative algorithms",
"recursive storytelling",
"distributed cognition"
]

cube = CubeGraph()
walker = SymbolicWalker(cube)

for c in concepts:

    start,path,seq,score = walker.run_concept(c)

    print("Concept:",c)
    print("Seed:",start)
    print("Path:",path)
    print("Sequence:","".join(seq))
    print("Score:",score)
    print()
