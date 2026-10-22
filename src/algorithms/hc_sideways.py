import time
from model.initial import initial_state
from model.objective import value
from algorithms.hc_steepest import find_neighbor


def sideways_move(vehicles, ship):
    start_time = time.perf_counter()
    max_sideways = 20

    current_state = initial_state(vehicles, ship)
    start_state = dict(current_state)

    sideways_moves = 0
    iterations = 0
    history = [value(current_state, vehicles)]

    while True:
        best_state, best_value = find_neighbor(current_state, vehicles, ship, allow_sideways=True)

        current_value = value(current_state, vehicles)
        iterations += 1

        if best_value > current_value:
            current_state = best_state
            sideways_moves = 0

        elif best_value == current_value and best_state != current_state:
            if sideways_moves >= max_sideways:
                history.append(current_value)
                break

            current_state = best_state
            sideways_moves += 1

        else:
            history.append(current_value)
            break

    final_state = current_state
    final_value = value(final_state, vehicles)
    duration = time.perf_counter() - start_time

    return{
        "initial_state": start_state,
        "final_state": final_state,
        "final_value": final_value,
        "iterations": iterations,
        "sideways_moves": sideways_moves,
        "history" : history, 
        "duration" : duration
    }