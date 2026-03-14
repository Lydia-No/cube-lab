def rotate(seq):

    if not seq:
        return seq

    return seq[1:] + seq[:1]


def score_sequence(seq):

    score = 0

    if seq == seq[::-1]:
        score += 5

    if len(set(seq)) < len(seq):
        score += 2

    if seq[0] == seq[-1]:
        score += 3

    return score
