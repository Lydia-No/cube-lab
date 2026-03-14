from cube_explorer.core import concept_seed, execute_sequence
from cube_explorer.grammars import get_grammar

def test_deterministic_same_output_twice() -> None:
    g = get_grammar("sefer")
    start = concept_seed("collective intelligence")
    seq = ["א", "מ", "ש", "א", "מ", "ש"]

    p1, s1, score1 = execute_sequence(start=start, symbols=seq, grammar=g)
    p2, s2, score2 = execute_sequence(start=start, symbols=seq, grammar=g)

    assert p1 == p2
    assert s1 == s2
    assert score1 == score2
