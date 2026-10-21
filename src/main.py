
import json
import time
from pathlib import Path

from model.entities import Vehicle, Ship, Dimensions
from model.objective import value
from model.validation import is_valid
from view.grid import show_grid

from algorithms.hc_steepest import steepest_ascent
from algorithms.hc_sideways import sideways_move
from algorithms.hc_random import random_restart
from algorithms.simulated_annealing import simulated_annealing
from algorithms.genetic import genetic_algorithm


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


def show_result(name, state, vehicles, ship, duration):
    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print("Shipping Fee:", value(state, vehicles))
    print("Valid:", is_valid(state, vehicles, ship))

    loaded = 0

    for placement in state.values():
        if placement is not None:
            loaded += 1

    print("Kendaraan Dimuat:", loaded, "/", len(vehicles))
    print("Waktu:", round(duration, 4), "detik")

    show_grid(state, vehicles, ship)


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
    state, iterations = steepest_ascent(vehicles, ship)
    duration = time.perf_counter() - start

    show_result(
        "1. Steepest Ascent",
        state,
        vehicles,
        ship,
        duration
    )
    print("Iterasi:", iterations)

    # 2. Sideways Move
    start = time.perf_counter()
    state, iterations, sideways_moves = sideways_move(vehicles, ship)
    duration = time.perf_counter() - start

    show_result(
        "2. Sideways Move",
        state,
        vehicles,
        ship,
        duration
    )
    print("Iterasi:", iterations)
    print("Jumlah sideways move:", sideways_moves)

    # 3. Random Restart
    start = time.perf_counter()
    state, restart_count, restart_iterations = random_restart(
        vehicles, ship
    )
    duration = time.perf_counter() - start

    show_result(
        "3. Random Restart",
        state,
        vehicles,
        ship,
        duration
    )
    print("Jumlah restart:", restart_count)
    print("Iterasi tiap restart:", restart_iterations)

    # 4. Simulated Annealing
    start = time.perf_counter()
    sa_result = simulated_annealing(
        vehicles=vehicles,
        ship=ship,
        initial_temp=100,
        alpha=0.95,
        max_iteration=1000,
        seed=21
    )
    duration = time.perf_counter() - start

    show_result(
        "4. Simulated Annealing",
        sa_result.final_state,
        vehicles,
        ship,
        duration
    )
    print("Iterasi:", sa_result.iterations)

    # 5. Genetic Algorithm
    start = time.perf_counter()
    ga_result = genetic_algorithm(
        vehicles=vehicles,
        ship=ship,
        pop_size=30,
        max_generations=100,
        p_mutation=0.1,
        seed=21
    )
    duration = time.perf_counter() - start

    show_result(
        "5. Genetic Algorithm",
        ga_result.final_state,
        vehicles,
        ship,
        duration
    )
    print("Generasi:", ga_result.iterations)
