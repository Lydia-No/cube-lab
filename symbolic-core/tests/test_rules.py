from symbolic_core.rules import LocalRule
from symbolic_core.state import SymbolicState


def test_rule_applies_and_flips():
    state = SymbolicState.from_string("1100")
    rule = LocalRule(condition_on=(0, 1), condition_off=(2,), flip_indices=(3,))
    assert rule.applies(state) is True

    out = rule.apply(state)
    assert out.to_string() == "1101"
