def gray_code(n):
    """
    Generate n-bit Gray code sequence.
    """

    if n == 0:
        return [""]

    prev = gray_code(n - 1)

    result = []

    for code in prev:
        result.append("0" + code)

    for code in reversed(prev):
        result.append("1" + code)

    return result


def gray_flip_sequence(gray):

    flips = []

    for i in range(1, len(gray)):

        a = gray[i - 1]
        b = gray[i]

        for j in range(len(a)):
            if a[j] != b[j]:
                flips.append(j)
                break

    return flips
