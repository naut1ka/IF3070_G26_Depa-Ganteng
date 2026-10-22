import json
import random
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from algorithms.genetic import genetic_algorithm
from algorithms.hc_random import random_restart
from algorithms.hc_sideways import sideways_move
from algorithms.hc_steepest import steepest_ascent
from algorithms.hc_stochastic import stochastic_hill_climbing
from algorithms.simulated_annealing import simulated_annealing
from model.entities import Dimensions, Ship, Vehicle
from view.genetic import show_genetic_result
from view.hill_climbing import (show_hill_climbing_result,show_stochastic_hill_climbing_result)
from view.simulated_annealing import show_simulated_annealing_result

DATA_PATH = Path(__file__).resolve().parent / "data" / "data.json"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "output"

def read_positive_integer(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Masukkan bilangan bulat positif.")
            continue

        if value > 0:
            return value
        print("Nilai harus lebih besar dari 0.")

def load_problem() -> tuple[dict[str, Vehicle], Ship]:
    with DATA_PATH.open(encoding="utf-8") as data_file:
        data = json.load(data_file)

    vehicles = {
        item["id"]: Vehicle(
            id=item["id"],
            shipping_fee=item["shipping_fee"],
            weight=item["weight"],
            eta=item["eta"],
            dimensions=Dimensions(w=item["w"], l=item["l"])
        )
        for item in data["vehicles"]
    }
    ship_data = data["ship"]
    ship = Ship(
        dimensions=Dimensions(w=ship_data["w"], l=ship_data["l"]),
        max_capacity=ship_data["max_capacity"]
    )
    return vehicles, ship

def serialize_state(state: dict) -> dict:
    return {
        vehicle_id: (
            None if placement is None
            else {
                "x": placement.x,
                "y": placement.y,
                "orientation": placement.orientation.value,
            }
        )
        for vehicle_id, placement in state.items()
    }

def get_result_field(result, name: str):
    if isinstance(result, dict):
        return result[name]
    return getattr(result, name)

def save_result(algorithm: str, result, parameters: dict, figure) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_directory = OUTPUT_PATH / f"{algorithm}_{timestamp}"
    run_directory.mkdir(parents=True, exist_ok=False)

    if hasattr(result, "mean_values"):
        objective_history = {
            "maximum": result.values,
            "average": result.mean_values
        }
    elif isinstance(result, dict):
        objective_history = result.get("history", result.get("values"))
    else:
        objective_history = result.values

    payload = {
        "algorithm": algorithm,
        "parameters": parameters,
        "initial_state": serialize_state(get_result_field(result, "initial_state")),
        "final_state": serialize_state(get_result_field(result, "final_state")),
        "final_objective": get_result_field(result, "final_value"),
        "iterations": get_result_field(result, "iterations"),
        "objective_history": objective_history,
        "duration_seconds": get_result_field(result, "duration")
    }
    if isinstance(result, dict):
        metrics = {
            key: result[key]
            for key in (
                "restart_count",
                "iterations_per_restart",
                "sideways_moves"
            )
            if key in result
        }
        if metrics:
            payload["metrics"] = metrics

    with (run_directory / "result.json").open("w", encoding="utf-8") as result_file:
        json.dump(payload, result_file, ensure_ascii=False, indent=2)
    figure.savefig(run_directory / "plot.png", dpi=150, bbox_inches="tight")
    return run_directory

def main() -> None:
    vehicles, ship = load_problem()
    print(
        f"Data dimuat: {len(vehicles)} kendaraan, "
        f"kapal {ship.dimensions.w} x {ship.dimensions.l}"
    )

    while True:
        RANDOM_SEED = random.random()
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
            parameters = {
                "pop_size": read_positive_integer("Jumlah populasi: "),
                "max_generations": read_positive_integer("Banyak iterasi: "),
                "p_mutation": 0.01,
                "seed": RANDOM_SEED
            }
            result = genetic_algorithm(
                vehicles=vehicles,
                ship=ship,
                pop_size=parameters["pop_size"],
                max_generations=parameters["max_generations"],
                p_mutation=parameters["p_mutation"],
                seed=parameters["seed"]
            )
            figure = show_genetic_result(
                result,
                vehicles,
                ship,
                show=False
            )
            algorithm_name = "genetic"

        elif choice == "2":
            parameters = {
                "initial_temp": 100.0,
                "alpha": 0.995,
                "max_iteration": 5000,
                "seed": RANDOM_SEED,
                "stuck_limit": 50,
                "min_temp": 1e-9
            }
            result = simulated_annealing(
                vehicles=vehicles,
                ship=ship,
                initial_temp=parameters["initial_temp"],
                alpha=parameters["alpha"],
                max_iteration=parameters["max_iteration"],
                seed=parameters["seed"],
                stuck_limit=parameters["stuck_limit"],
                min_temp=parameters["min_temp"]
            )
            figure = show_simulated_annealing_result(
                result,
                vehicles,
                ship,
                show=False,
                parameters=parameters
            )
            algorithm_name = "simulated_annealing"

        elif choice == "3":
            result = steepest_ascent(vehicles, ship)
            figure = show_hill_climbing_result(
                result,
                vehicles,
                ship,
                variant="steepest",
                show=False
            )
            algorithm_name = "hill_climbing_steepest"

        elif choice == "4":
            parameters = {"max_restarts": 10}
            result = random_restart(vehicles, ship)
            figure = show_hill_climbing_result(
                result,
                vehicles,
                ship,
                variant="random_restart",
                show=False,
            )
            algorithm_name = "hill_climbing_random_restart"

        elif choice == "5":
            parameters = {"max_sideways": 20}
            result = sideways_move(vehicles, ship)
            figure = show_hill_climbing_result(
                result,
                vehicles,
                ship,
                variant="sideways",
                show=False,
            )
            algorithm_name = "hill_climbing_sideways"

        else:
            result = stochastic_hill_climbing(vehicles, ship)
            figure = show_stochastic_hill_climbing_result(
                result, vehicles, ship, show=False
            )
            algorithm_name = "hill_climbing_stochastic"

        run_directory = save_result(algorithm_name, result, parameters, figure)
        print(f"Hasil tersimpan di: {run_directory}")
        plt.show()
        plt.close(figure)


if __name__ == "__main__":
    main()