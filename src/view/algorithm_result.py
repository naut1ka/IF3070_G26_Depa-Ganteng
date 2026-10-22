from collections.abc import Mapping, Sequence
import random

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from model.entities import Ship, State, Vehicle
from model.objective import value


OBJECTIVE_COLOR = "#4C78A8"

def get_vehicle_color(vehicle_id: str) -> str:
    rng = random.Random(vehicle_id)
    channels = [rng.randint(50, 200) for _ in range(3)]
    return "#{:02x}{:02x}{:02x}".format(*channels)

def result_value(result: object, name: str):
    if isinstance(result, Mapping):
        return result[name]
    return getattr(result, name)

def draw_state(axes: Axes, state: State, vehicles: Mapping[str, Vehicle], ship: Ship, title: str) -> None:
    axes.set_title(title)
    axes.set_xlim(0, ship.dimensions.w)
    axes.set_ylim(ship.dimensions.l, 0)
    axes.set_aspect("equal")
    axes.set_xticks(range(ship.dimensions.w + 1))
    axes.set_yticks(range(ship.dimensions.l + 1))
    axes.grid(color="#D7DCE2", linewidth=0.8)
    axes.set_axisbelow(True)
    axes.set_xlabel("Posisi X")
    axes.set_ylabel("Posisi Y")

    for vehicle_id, placement in state.items():
        if placement is None:
            continue

        vehicle = vehicles[vehicle_id]
        width, height = vehicle.effective_size(placement.orientation)
        axes.add_patch(
            Rectangle((placement.x, placement.y), width, height, facecolor=get_vehicle_color(vehicle_id), edgecolor="white", linewidth=1.5)
        )
        axes.text(placement.x + width / 2, placement.y + height / 2, vehicle_id, color="red", ha="center", va="center", fontsize=6, fontweight="bold", clip_on=True)

def make_algorithm_result_figure(
    title: str,
    result: object,
    vehicles: Mapping[str, Vehicle],
    ship: Ship,
    stats: Sequence[str],
    duration: float | None,
    objective_series: Sequence[tuple[str, Sequence[float], str]] | None = None
) -> Figure:
    initial_state = result_value(result, "initial_state")
    final_state = result_value(result, "final_state")
    final_value = result_value(result, "final_value")
    iterations = result_value(result, "iterations")

    figure = plt.figure(figsize=(12, 8))
    layout = figure.add_gridspec(2, 2, height_ratios=(1, 0.85))
    initial_axes = figure.add_subplot(layout[0, 0])
    final_axes = figure.add_subplot(layout[0, 1])
    objective_axes = figure.add_subplot(layout[1, :])

    draw_state(initial_axes, initial_state, vehicles, ship, "State Awal")
    draw_state(final_axes, final_state, vehicles, ship, "State Akhir")

    if isinstance(result, Mapping) and "history" in result:
        history = list(result["history"])
        if history:
            objective_axes.plot(
                range(len(history)),
                history,
                color=OBJECTIVE_COLOR,
                linewidth=2,
                marker="o",
                markersize=3
            )
    elif isinstance(result, Mapping):
        initial_value = value(initial_state, vehicles)
        final_value_at_state = value(final_state, vehicles)
        objective_axes.scatter(
            [0, iterations],
            [initial_value, final_value_at_state],
            color=OBJECTIVE_COLOR,
            zorder=3
        )
        objective_axes.set_xlim(left=0, right=max(iterations, 1))
        objective_axes.text(
            0.01,
            0.97,
            "Riwayat objective tidak tersedia; hanya state awal/akhir ditampilkan.",
            transform=objective_axes.transAxes,
            ha="left",
            va="top",
            fontsize=8,
            color="#555555"
        )
    elif objective_series is not None:
        for label, series, color in objective_series:
            objective_axes.plot(
                range(1, len(series) + 1),
                series,
                color=color,
                label=label,
                linewidth=2
            )
        objective_axes.legend()
    else:
        history = list(result_value(result, "values"))
        initial_value = value(initial_state, vehicles)
        points = [initial_value, *history]
        iterations_axis = range(len(points))
        objective_axes.plot(
            iterations_axis,
            points,
            color=OBJECTIVE_COLOR,
            linewidth=2,
            marker="o",
            markersize=3
        )

    objective_axes.set_title("Nilai Objective Function per Iterasi")
    objective_axes.set_xlabel(
        "Urutan nilai riwayat (restart digabung)" if isinstance(result, Mapping) else "Iterasi"
    )
    objective_axes.set_ylabel("Nilai Objective Function")
    objective_axes.grid(color="#D7DCE2", linewidth=0.8, alpha=0.8)

    if duration is None:
        duration = (
            result.get("duration")
            if isinstance(result, Mapping)
            else getattr(result, "duration", None)
        )
    duration_text = (
        f"Duration: {duration:.4f} seconds"
        if duration is not None
        else "Duration: not available"
    )
    summary = [f"Final Objective: {final_value}", duration_text, *stats]
    figure.suptitle(title, fontsize=15, fontweight="bold")
    figure.text(0.5, 0.925, "\n".join(summary), ha="center", va="top", fontsize=9)
    figure.tight_layout(rect=(0, 0, 1, 0.82))
    return figure
