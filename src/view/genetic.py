import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from algorithms.genetic import GAResult
from model.entities import Ship, Vehicle
from view._algorithm_result import make_algorithm_result_figure


def show_genetic_result(result: GAResult, vehicles: dict[str, Vehicle], ship: Ship, show: bool = True) -> Figure:
    stats = (
        f"Ukuran populasi: {result.population_size}",
        f"Generasi: {result.iterations}",
        f"Elite: {result.elite_size}",
        f"Probabilitas mutasi: {result.mutation_rate:.2%}",
        f"Stagnasi: {result.stuck_count} kali",
    )
    figure = make_algorithm_result_figure("Hasil Genetic Algorithm", result, vehicles, ship, stats)
    if show:
        plt.show()
    return figure
