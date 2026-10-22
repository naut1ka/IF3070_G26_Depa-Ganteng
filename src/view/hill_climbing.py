import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from model.entities import Ship, Vehicle
from view.algorithm_result import make_algorithm_result_figure


def show_hill_climbing_result(
    result: dict,
    vehicles: dict[str, Vehicle],
    ship: Ship,
    variant: str = "steepest",
    show: bool = True,
    duration: float | None = None
) -> Figure:
    if variant == "random_restart":
        stats = [f"Iterations in best run: {result['iterations']}"]
    else:
        stats = [f"Iterations: {result['iterations']}"]

    if variant == "random_restart":
        stats.extend(
            (
                f"Total restarts: {result['restart_count']}",
                f"Iterations per run: {result['iterations_per_restart']}"
            )
        )
    elif variant == "sideways":
        stats.extend(
            (
                "Sideways moves at termination "
                f"(reset after an uphill move): {result['sideways_moves']}"
            )
        )
    elif variant == "stochastic":
        pass
    elif variant != "steepest":
        raise ValueError(f"Unknown Hill Climbing variant: {variant}")

    figure = make_algorithm_result_figure(
        f"Hill Climbing Results ({variant.replace('_', ' ').title()})",
        result,
        vehicles,
        ship,
        stats,
        duration
    )

    if show:
        plt.show()
    return figure


def show_stochastic_hill_climbing_result(
    result: dict,
    vehicles: dict[str, Vehicle],
    ship: Ship,
    show: bool = True,
    duration: float | None = None
) -> Figure:
    return show_hill_climbing_result(
        result,
        vehicles,
        ship,
        variant="stochastic",
        show=show,
        duration=duration
    )