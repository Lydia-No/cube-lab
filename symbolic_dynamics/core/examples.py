from .subshift import Subshift


def golden_mean_shift():

    return Subshift(
        alphabet=["0", "1"],
        forbidden=["11"]
    )


def even_shift():

    return Subshift(
        alphabet=["0", "1"],
        forbidden=["101"]
    )


def no_three_consecutive_ones():

    return Subshift(
        alphabet=["0", "1"],
        forbidden=["111"]
    )
