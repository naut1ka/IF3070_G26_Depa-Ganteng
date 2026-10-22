import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from algorithms.genetic import GAResult
from model.entities import Ship, Vehicle
from view.algorithm_result import make_algorithm_result_figure


def show_genetic_result(
    result: GAResult,
    vehicles: dict[str, Vehicle],
    ship: Ship,
    show: bool = True,
    duration: float | None = None
) -> Figure:
    stats = (
        f"Population Size: {result.population_size}",
        f"Iteration Count: {result.iterations}"
    )
    actual_duration = result.duration if duration is None else duration
    figure = make_algorithm_result_figure(
        "Hasil Genetic Algorithm",
        result,
        vehicles,
        ship,
        stats,
        actual_duration,
        objective_series=(
            ("Population Objective Max", result.values, "#4166F5"),
            ("Population Objective Mean", result.mean_values, "#C71585"),
        )
    )
    if show:
        plt.show()
    return figure
