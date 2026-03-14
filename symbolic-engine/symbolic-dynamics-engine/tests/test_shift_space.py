from symbolic_dynamics.core.shift_space import ShiftSpace


def test_random_configuration():

    shift = ShiftSpace(["0","1"])

    config = shift.random_configuration(10)

    assert len(config.data) == 10
