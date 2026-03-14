from symbolic_dynamics.geometry.cube.cube_shift import CubeShift


def test_cube_creation():

    cube = CubeShift(["0","1"],3)

    assert cube.state.shape == (3,3,3)
