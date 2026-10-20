
from .entities import Ship, Vehicle

def value(state: Ship.State, vehicles: dict[str, Vehicle]) -> int:
    
    total_value = 0

    for vehicle_id, placement in state.items():
        if placement is None:
            continue
        total_value += vehicles[vehicle_id].shipping_fee

    return total_value
