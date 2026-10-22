import json
import random
from pathlib import Path

from algorithms.genetic import genetic_algorithm
from algorithms.hc_random import random_restart
from algorithms.hc_sideways import sideways_move
from algorithms.hc_steepest import steepest_ascent
from algorithms.hc_stochastic import stochastic_hill_climbing
from algorithms.simulated_annealing import simulated_annealing
from model.entities import Dimensions, Ship, Vehicle
from view.genetic import show_genetic_result
from view.hill_climbing import (show_hill_climbing_result,show_stochastic_hill_climbing_result,)
from view.simulated_annealing import show_simulated_annealing_result

DATA_PATH = Path(__file__).resolve().parent / "data" / "data.json"
RANDOM_SEED = random.random()

def load_problem() -> tuple[dict[str, Vehicle], Ship]:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        data = json.load(data_file)

    vehicles = {
        item["id"]: Vehicle(
            id=item["id"],
            shipping_fee=item["shipping_fee"],
            weight=item["weight"],
            eta=item["eta"],
            dimensions=Dimensions(w=item["w"], l=item["l"]),
        )
        for item in data["vehicles"]
    }
    ship_data = data["ship"]
    ship = Ship(
        dimensions=Dimensions(w=ship_data["w"], l=ship_data["l"]),
        max_capacity=ship_data["max_capacity"],
    )
    return vehicles, ship


def main() -> None:
    vehicles, ship = load_problem()
    print(
        f"Data dimuat: {len(vehicles)} kendaraan, "
        f"kapal {ship.dimensions.w} x {ship.dimensions.l}"
    )

    while True:
        print(
            "\nPilih algoritma:"
            "\n  1. Genetic Algorithm"
            "\n  2. Simulated Annealing"
            "\n  3. Hill Climbing - Steepest Ascent"
            "\n  4. Hill Climbing - Random Restart"
            "\n  5. Hill Climbing - Sideways Move"
            "\n  6. Hill Climbing - Stochastic"
            "\n  0. Keluar"
        )
        choice = input("Pilihan: ").strip()

        if choice == "0":
            print("Program selesai.")
            return
        if choice not in {"1", "2", "3", "4", "5", "6"}:
            print("Pilihan tidak valid. Masukkan angka 0 sampai 6.")
            continue

        if choice == "1":
            result = genetic_algorithm(
                vehicles=vehicles,
                ship=ship,
                pop_size=50,
                max_generations=100,
                p_mutation=0.1,
                seed=RANDOM_SEED,
            )
            show_genetic_result(result, vehicles, ship)
        elif choice == "2":
            result = simulated_annealing(
                vehicles=vehicles,
                ship=ship,
                initial_temp=100.0,
                alpha=0.95,
                max_iteration=500,
                seed=RANDOM_SEED,
            )
            show_simulated_annealing_result(result, vehicles, ship)
        elif choice == "3":
            random.seed(RANDOM_SEED)
            result = steepest_ascent(vehicles, ship)
            show_hill_climbing_result(result, vehicles, ship, variant="steepest")
        elif choice == "4":
            random.seed(RANDOM_SEED)
            result = random_restart(vehicles, ship)
            show_hill_climbing_result(
                result, vehicles, ship, variant="random_restart"
            )
        elif choice == "5":
            random.seed(RANDOM_SEED)
            result = sideways_move(vehicles, ship)
            show_hill_climbing_result(result, vehicles, ship, variant="sideways")
        else:
            random.seed(RANDOM_SEED)
            result = stochastic_hill_climbing(vehicles, ship)
            show_stochastic_hill_climbing_result(result, vehicles, ship)


if __name__ == "__main__":
    main()