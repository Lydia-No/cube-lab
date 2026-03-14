from symbolic_core.state import SymbolicState


def test_state_from_string():
    s = SymbolicState.from_string("0101")
    assert s.bits == (0, 1, 0, 1)
    assert s.to_string() == "0101"


def test_flip():
    s = SymbolicState.from_string("0000")
    s2 = s.flip(2)
    assert s2.to_string() == "0010"
