
from model.objective import value
from algorithms.hc_steepest import steepest_ascent


def random_restart(vehicles, ship, max_restarts, max_iterations):
    best_state = None
    best_value = -1

    for _ in range(max_restarts):
        current_state = steepest_ascent(vehicles, ship, max_iterations)
        current_value = value(current_state, vehicles)

        if current_value > best_value:
            best_state = current_state
            best_value = current_value

    return best_state
