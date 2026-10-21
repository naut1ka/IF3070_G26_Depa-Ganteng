from model.objective import value
from algorithms.hc_steepest import steepest_ascent


def random_restart(vehicles, ship):
    max_restarts = 10
    best_state = None
    best_value = -1
    restart_count = 0
    iterations_per_restart = []

    for i in range(max_restarts):
        current_state, iterations = steepest_ascent(vehicles, ship)
        current_value = value(current_state, vehicles)

        restart_count += 1
        iterations_per_restart.append(iterations)

        if current_value > best_value:
            best_state = current_state
            best_value = current_value

    return best_state, restart_count, iterations_per_restart
