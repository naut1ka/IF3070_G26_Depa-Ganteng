
import json
import time
from pathlib import Path

from model.entities import Vehicle, Ship, Dimensions
from model.objective import value
from model.validation import is_valid
from view.grid import show_grid

from algorithms.hc_steepest import steepest_ascent
from algorithms.hc_stochastic import stochastic_hill_climbing
from algorithms.hc_sideways import sideways_move
from algorithms.hc_random import random_restart


def load_data():
    folder = Path(__file__).resolve().parent

    with open(folder / "data" / "data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    vehicles = {}

    for item in data["vehicles"]:
        vehicle = Vehicle(
            id=item["id"],
            shipping_fee=item["shipping_fee"],
            weight=item["weight"],
            eta=item["eta"],
            dimensions=Dimensions(item["w"], item["l"])
        )

        vehicles[vehicle.id] = vehicle

    ship_data = data["ship"]

    ship = Ship(
        dimensions=Dimensions(ship_data["w"], ship_data["l"]),
        max_capacity=ship_data["max_capacity"]
    )

    return vehicles, ship


def show_result(name, result, vehicles, ship, duration):
    initial = result["initial_state"]
    final = result["final_state"]

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print("Final Objective:", result["final_value"])
    print("Valid:", is_valid(final, vehicles, ship))

    loaded = sum(
        1 for placement in final.values()
        if placement is not None
    )

    print("Kendaraan Dimuat:", loaded, "/", len(vehicles))
    print("Duration:", round(duration, 4), "detik")

    print("\nGrid Awal:")
    show_grid(initial, vehicles, ship)

    print("\nGrid Akhir:")
    show_grid(final, vehicles, ship)


if __name__ == "__main__":
    vehicles, ship = load_data()

    print("Jumlah kendaraan:", len(vehicles))
    print(
        "Ukuran kapal:",
        ship.dimensions.w,
        "x",
        ship.dimensions.l
    )
    print("Kapasitas:", ship.max_capacity)

    # 1. Steepest Ascent
    start = time.perf_counter()
    result = steepest_ascent(vehicles, ship)
    duration = time.perf_counter() - start

    show_result(
        "1. Steepest Ascent",
        result, vehicles, ship, duration
    )
    print("Iterations:", result["iterations"])

    # 2. Stochastic Hill-Climbing
    start = time.perf_counter()
    result = stochastic_hill_climbing(vehicles, ship)
    duration = time.perf_counter() - start

    show_result(
        "2. Stochastic Hill-Climbing",
        result, vehicles, ship, duration
    )
    print("Iterations:", result["iterations"])

    # 3. Sideways Move
    start = time.perf_counter()
    result = sideways_move(vehicles, ship)
    duration = time.perf_counter() - start

    show_result(
        "3. Hill-Climbing with Sideways Move",
        result, vehicles, ship, duration
    )
    print("Iterations:", result["iterations"])
    print("Sideways Moves:", result["sideways_moves"])

    # 4. Random Restart
    start = time.perf_counter()
    result = random_restart(vehicles, ship)
    duration = time.perf_counter() - start

    show_result(
        "4. Random Restart Hill-Climbing",
        result, vehicles, ship, duration
    )
    print("Iterations (best restart):", result["iterations"])
    print("Restart Count:", result["restart_count"])
    print("Iterations per Restart:", result["iterations_per_restart"])
    print(
        "Total Iterations:",
        sum(result["iterations_per_restart"])
    )
