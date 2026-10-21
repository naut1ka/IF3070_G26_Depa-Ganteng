
from model.entities import Vehicle, Ship, Dimensions
from algorithms.hc_random import random_restart
from model.objective import value
from model.validation import is_valid
from view.grid import show_grid

if __name__ == "__main__":
    ship = Ship(Dimensions(4, 2), 500)

    vehicles = [
        Vehicle("Dheva", 60, 6, 4, Dimensions(2, 2)),
        Vehicle("Afif", 60, 6, 4, Dimensions(2, 1)),
        Vehicle("Falzi", 60, 6, 4, Dimensions(2, 2))
    ]

    vehicles_by_id = {}

    for vehicle in vehicles:
        vehicles_by_id[vehicle.id] = vehicle

    max_restarts = 20
    max_iterations = 100

    best_state = random_restart(
        vehicles_by_id,
        ship,
        max_restarts,
        max_iterations
    )

    best_value = value(best_state, vehicles_by_id)

    print("Hasil Random Restart")
    print("Total Shipping Fee:", best_value, "juta rupiah")
    print("Valid:", is_valid(best_state, vehicles_by_id, ship))
    print("State:", best_state)

    show_grid(best_state, vehicles_by_id, ship)
