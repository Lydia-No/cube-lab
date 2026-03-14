def detect_cycle(trajectory):

    seen = {}

    for i, state in enumerate(trajectory):

        if state in seen:

            start = seen[state]

            cycle = trajectory[start:i]

            return {
                "cycle_start": start,
                "cycle_length": len(cycle),
                "cycle_states": cycle
            }

        seen[state] = i

    return None
