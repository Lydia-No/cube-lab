from symbolic_core.state import SymbolicState
from symbolic_core.rule import PermutationRule
from symbolic_core.engine import DynamicsEngine

def test_core_engine_step():
    s = SymbolicState(["A","B","C"])
    rule = PermutationRule(0,1)
    engine = DynamicsEngine([rule])
    new_state = engine.step(s)
    assert new_state.symbols == ("B","A","C")
