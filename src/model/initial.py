import random
from model.entities import Vehicle, Ship, Placement, Orientation, State
from model.validation import is_valid

def initial_state(vehicles: dict[str, Vehicle], ship: Ship) -> State:
    state = {vehicle_id: None for vehicle_id in vehicles}
    names = list(vehicles)
    random.shuffle(names)

    for name in names:
        vehicle = vehicles[name]

        for _ in range(20):
            orientation = random.choice(list(Orientation))
            cols, rows = vehicle.effective_size(orientation)

            max_x = ship.dimensions.w - cols
            max_y = ship.dimensions.l - rows
            if max_x < 0 or max_y < 0:
                continue
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)

            candidate = dict(state)
            candidate[name] = Placement(x, y, orientation)

            if is_valid(candidate, vehicles, ship):
                state = candidate
                break

    return state
