from symbolic_core.search.beam import search_rules
from symbolic_core.state import SymbolicState


def test_search_rules_returns_candidates():
    initial = SymbolicState.from_string("0101")
    top = search_rules(initial=initial, n_bits=4, steps=8, top_k=5)
    assert len(top) == 5
    assert top[0].score >= top[-1].score
