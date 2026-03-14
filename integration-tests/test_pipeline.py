from symbolic_core.state import SymbolicState
from symbolic_core.rule import PermutationRule
from symbolic_core.engine import DynamicsEngine

def test_engine_pipeline():
    state = SymbolicState(["A","B","C","D"])
    rules = [
        PermutationRule(0,1),
        PermutationRule(2,3)
    ]
    engine = DynamicsEngine(rules)
    history = engine.run(state, 10)
    assert len(history) == 11
