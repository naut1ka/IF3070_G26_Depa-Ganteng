
from model.initial import initial_state
from model.objective import value
from algorithms.hc_steepest import find_neighbor


def sideways_move(vehicles, ship):
    max_sideways = 20
    current_state = initial_state(vehicles, ship)
    sideways_moves = 0
    iterations = 0

    while True:
        best_state, best_value = find_neighbor(current_state, vehicles, ship, allow_sideways=True)

        current_value = value(current_state, vehicles)
        iterations += 1

        if best_value > current_value:
            current_state = best_state
            sideways_moves = 0

        elif best_value == current_value and best_state != current_state:
            if sideways_moves >= max_sideways:
                break

            current_state = best_state
            sideways_moves += 1

        else:
            break

    return current_state, iterations, sideways_moves
