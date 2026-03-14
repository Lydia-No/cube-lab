def compute_orbit(configuration, steps):

    orbit = []

    current = configuration

    for _ in range(steps):

        orbit.append(current)

        current = current.shift()

    return orbit
