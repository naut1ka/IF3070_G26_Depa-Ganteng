
from .entities import Ship, Vehicle, Placement, Orientation

def is_valid(state: Ship.State, vehicles: dict[str, Vehicle], ship: Ship) -> bool:
    if state.keys() != vehicles.keys():
        return False

    occupied = set()
    total_weight = 0

    for vehicle_id, placement in state.items():
        if placement is None:
            continue

        vehicle = vehicles[vehicle_id]

        if not isinstance(placement, Placement):
            return False

        if not isinstance(placement.orientation, Orientation):
            return False

        cells = vehicle.occupied_cells(placement)

        for x, y in cells:
            if x < 0 or x >= ship.dimensions.w:
                return False

            if y < 0 or y >= ship.dimensions.l:
                return False

            if (x, y) in occupied:
                return False

            occupied.add((x, y))

        total_weight += vehicle.weight

    if total_weight > ship.max_capacity:
        return False

    return True
