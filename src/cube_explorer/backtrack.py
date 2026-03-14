def backtrack_rate(seq):

    repeats = 0

    for i in range(1, len(seq)):

        if seq[i] == seq[i-1]:
            repeats += 1

    return repeats / (len(seq) - 1)


def analyze_backtracking(cube, steps):

    seq = cube.random_walk(steps)

    rate = backtrack_rate(seq)

    return seq, rate
