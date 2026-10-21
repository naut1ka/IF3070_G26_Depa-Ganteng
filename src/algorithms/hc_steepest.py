
from model.initial import initial_state
from model.neighbor import move, swap
from model.validation import is_valid
from model.objective import value
from model.entities import Placement, Orientation


def find_best_neighbor(current_state, vehicles, ship):
    best_state = current_state
    best_value = value(current_state, vehicles)

    for v_id in vehicles:
        vehicle = vehicles[v_id]
        posisi = current_state[v_id]

        if posisi == None:
            for orient in Orientation:
                cols, rows = vehicle.effective_size(orient)

                for y in range(ship.dimensions.l - rows + 1):
                    for x in range(ship.dimensions.w - cols + 1):
                        new_state = dict(current_state)
                        new_state[v_id] = Placement(x, y, orient)

                        if is_valid(new_state, vehicles, ship) == True:
                            new_value = value(new_state, vehicles)

                            if new_value> best_value:
                                best_state = new_state
                                best_value = new_value

        else:
            for orient in Orientation:
                new_state = dict(current_state)
                new_state[v_id] =Placement(posisi.x, posisi.y, orient)

                if is_valid(new_state, vehicles, ship) == True:
                    new_value = value(new_state, vehicles)

                    if new_value > best_value:
                        best_state = new_state
                        best_value = new_value

            for y in range(ship.dimensions.l):
                for x in range(ship.dimensions.w):
                    new_state = move(current_state, v_id, x, y)

                    if is_valid(new_state, vehicles, ship) == True:
                        new_value = value(new_state, vehicles)

                        if new_value > best_value:
                            best_state = new_state
                            best_value = new_value

    vehicle_ids = list(vehicles.keys())

    for i in range(len(vehicle_ids)):
        for j in range(i + 1, len(vehicle_ids)):
            new_state = swap(current_state, vehicle_ids[i], vehicle_ids[j])

            if is_valid(new_state, vehicles, ship) == True:
                new_value = value(new_state, vehicles)

                if new_value > best_value:
                    best_state = new_state
                    best_value = new_value

    return best_state, best_value


def steepest_ascent(vehicles, ship, max_iterations):
    current_state = initial_state(vehicles, ship)

    for i in range(max_iterations):
        best_state, best_value = find_best_neighbor(current_state, vehicles, ship)
        current_value = value(current_state, vehicles)

        if best_value <= current_value:
            break

        current_state = best_state

    return current_state
