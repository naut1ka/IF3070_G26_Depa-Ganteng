import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from algorithms.simulated_annealing import SAResult
from model.entities import Ship, Vehicle
from view._algorithm_result import make_algorithm_result_figure


def show_simulated_annealing_result(result: SAResult, vehicles: dict[str, Vehicle], ship: Ship, show: bool = True) -> Figure:
    stats = (
        f"Iterasi: {result.iterations}",
        f"Batas iterasi: {result.max_iterations}",
        f"Suhu awal: {result.initial_temp:g}",
        f"Faktor pendinginan (alpha): {result.alpha:g}",
        f"Suhu minimum: {result.min_temp:g}",
        f"Stagnasi: {result.stuck_count} kali",
    )
    figure = make_algorithm_result_figure("Hasil Simulated Annealing", result, vehicles, ship, stats)
    if show:
        plt.show()
    return figure
