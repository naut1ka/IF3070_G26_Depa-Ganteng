from collections.abc import Mapping

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from algorithms.simulated_annealing import SAResult
from model.entities import Ship, Vehicle
from view.algorithm_result import make_algorithm_result_figure


def show_simulated_annealing_result(
    result: SAResult,
    vehicles: dict[str, Vehicle],
    ship: Ship,
    show: bool = True,
    duration: float | None = None,
    parameters: Mapping[str, object] | None = None
) -> Figure:
    stats = [f"Iterasi: {result.iterations}"]
    if parameters is not None:
        stats.extend(
            (
                f"Initial Temp: {parameters['initial_temp']:g}",
                f"alpha: {parameters['alpha']:g}",
                f"Max Iteration: {parameters['max_iteration']}",
                f"Stuck Limit: {parameters['stuck_limit']}"
            )
        )
    stats.append(f"Stuck Count: {result.stuck_count} kali")
    actual_duration = result.duration if duration is None else duration
    figure = make_algorithm_result_figure(
        "Hasil Simulated Annealing",
        result,
        vehicles,
        ship,
        stats,
        actual_duration
    )
    if show:
        plt.show()
    return figure
