from symbolic_dynamics.grammars.grammar_learning import GrammarLearner


sequence = ["cave","horse","cave","storm"]

trajectory = [
    (0,0,0),
    (1,0,0),
    (1,1,0),
    (2,1,0),
    (2,1,1)
]

learner = GrammarLearner()

grammar = learner.learn_from_sequence(sequence, trajectory)

print("Learned grammar:")
print(grammar)
