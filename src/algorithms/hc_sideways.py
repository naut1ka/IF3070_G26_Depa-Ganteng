
from model.initial import initial_state
from model.objective import value
from algorithms.hc_steepest import find_best_neighbor


def sideways_move(vehicles, ship, max_iterations, max_sideways):
    current_state = initial_state(vehicles, ship)
    sideways_moves = 0

    for i in range(max_iterations):
        best_state, best_value = find_best_neighbor(current_state, vehicles, ship, True)
        current_value = value(current_state, vehicles)

        if best_value > current_value:
            current_state = best_state
            sideways_moves = 0

        elif best_value == current_value and best_state != current_state:
            if sideways_moves >= max_sideways:
                break

            current_state = best_state
            sideways_moves += 1

            if sideways_moves >= max_sideways:
                break

        else:
            break

    return current_state
