from cube_explorer.grammars.mimulus import (
    flip_dimension,
    permute_axes,
    walk_sequence,
    state_to_bits,
)

def test_flip_dimension_twice_returns_original():
    state = 0
    state = flip_dimension(state, 2)
    state = flip_dimension(state, 2)
    assert state == 0

def test_permute_axes_identity():
    state = 0b10101
    result = permute_axes(state, [0,1,2,3,4])
    assert result == state

def test_walk_sequence_returns_path():
    seq = ["cave","horse","rotate_forward","storm"]
    path = walk_sequence(0, seq)
    assert len(path) == len(seq) + 1

def test_state_to_bits():
    assert state_to_bits(3) == "00011"
