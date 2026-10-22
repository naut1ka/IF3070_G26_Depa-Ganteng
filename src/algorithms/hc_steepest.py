from model.initial import initial_state
from model.neighbor import move, swap
from model.validation import is_valid
from model.objective import value
from model.entities import Placement, Orientation
import time


def find_neighbor(current_state, vehicles, ship, allow_sideways=False):
    current_value = value(current_state, vehicles)
    best_state = current_state
    best_value = current_value
    sideways_state = None

    for v_id in vehicles:
        vehicle = vehicles[v_id]
        posisi = current_state[v_id]

        if posisi is None:
            for orient in Orientation:
                cols, rows = vehicle.effective_size(orient)

                for y in range(ship.dimensions.l - rows + 1):
                    for x in range(ship.dimensions.w - cols + 1):
                        new_state = dict(current_state)
                        new_state[v_id] = Placement(x, y, orient)

                        if is_valid(new_state, vehicles, ship):
                            new_value = value(new_state, vehicles)

                            if new_value > best_value:
                                best_state = new_state
                                best_value = new_value

                            elif allow_sideways and new_value == current_value:
                                if new_state != current_state and sideways_state is None:
                                    sideways_state = new_state

        else:
            for orient in Orientation:
                new_state = dict(current_state)
                new_state[v_id] = Placement(posisi.x, posisi.y, orient)

                if is_valid(new_state, vehicles, ship):
                    new_value = value(new_state, vehicles)

                    if new_value > best_value:
                        best_state = new_state
                        best_value = new_value

                    elif allow_sideways and new_value == current_value:
                        if new_state != current_state and sideways_state is None:
                            sideways_state = new_state

            for y in range(ship.dimensions.l):
                for x in range(ship.dimensions.w):
                    new_state = move(current_state, v_id, x, y)

                    if is_valid(new_state, vehicles, ship):
                        new_value = value(new_state, vehicles)

                        if new_value > best_value:
                            best_state = new_state
                            best_value = new_value

                        elif allow_sideways and new_value == current_value:
                            if new_state != current_state and sideways_state is None:
                                sideways_state = new_state

    vehicle_ids = list(vehicles.keys())

    for i in range(len(vehicle_ids)):
        for j in range(i + 1, len(vehicle_ids)):
            new_state = swap(current_state, vehicle_ids[i], vehicle_ids[j])

            if is_valid(new_state, vehicles, ship):
                new_value = value(new_state, vehicles)

                if new_value > best_value:
                    best_state = new_state
                    best_value = new_value

                elif allow_sideways and new_value == current_value:
                    if new_state != current_state and sideways_state is None:
                        sideways_state = new_state

    if best_value > current_value:
        return best_state, best_value

    if allow_sideways and sideways_state is not None:
        return sideways_state, current_value

    return current_state, current_value


def steepest_ascent(vehicles, ship):
    start_time = time.perf_counter()
    current_state = initial_state(vehicles, ship)
    start_state = dict(current_state)
    iterations = 0
    history = [value(current_state, vehicles)]

    while True:
        best_state, best_value = find_neighbor(current_state, vehicles, ship)
        current_value = value(current_state, vehicles)
        iterations += 1
        
        if best_value <= current_value:
            break

        current_state = best_state
        history.append(value(current_state, vehicles))

    final_state = current_state
    final_value = value(final_state, vehicles)
    duration = time.perf_counter() - start_time

    return {
        "initial_state": start_state,
        "final_state": final_state,
        "final_value": final_value,
        "iterations": iterations,
        "history" : history,
        "duration": duration
    }