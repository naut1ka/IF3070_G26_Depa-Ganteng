import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from model.entities import Ship, Vehicle
from view._algorithm_result import make_algorithm_result_figure


def show_hill_climbing_result(result: dict,vehicles: dict[str, Vehicle], ship: Ship, variant: str = "steepest",show: bool = True) -> Figure:
    stats = [f"Iterasi: {result['iterations']}"]

    if variant == "random_restart":
        stats.extend(
            (f"Restart: {result['restart_count']} kali",
             f"Iterasi per restart: {result['iterations_per_restart']}")
        )
    elif variant == "sideways":
        stats.extend(
            (f"Sideways move: {result['sideways_moves']} kali",
             f"Batas sideways: {result['max_sideways_moves']} kali")
        )
    elif variant == "stochastic":
        stats.append(
            "Kandidat tetangga lebih baik yang dipertimbangkan: "
            f"{result['neighbor_candidates_considered']}"
        )

    figure = make_algorithm_result_figure(f"Hasil Hill Climbing ({variant.replace('_', ' ').title()})", result, vehicles,ship,stats)

    if show:
        plt.show()
    return figure


def show_stochastic_hill_climbing_result(result: dict,vehicles: dict[str, Vehicle], ship: Ship,show: bool = True) -> Figure:
    return show_hill_climbing_result(result,vehicles,ship,variant="stochastic",show=show)
