from collections.abc import Mapping, Sequence
import random

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from model.entities import Ship, State, Vehicle

def get_vehicle_color(vehicle_id: str) -> str:
    rng = random.Random(vehicle_id)
    r = rng.randint(50, 200)
    g = rng.randint(50, 200)
    b = rng.randint(50, 200)

    return f"#{r:02x}{g:02x}{b:02x}"

OBJECTIVE_COLOR = "#4C78A8"

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

def make_algorithm_result_figure(title: str, result: object, vehicles: Mapping[str, Vehicle], ship: Ship, stats: Sequence[str]) -> Figure:
    initial_state = result_value(result, "initial_state")
    final_state = result_value(result, "final_state")
    final_value = result_value(result, "final_value")
    duration = result_value(result, "duration")
    is_hill_climbing_result = isinstance(result, Mapping)
    values = (
        result_value(result, "objective_history") if is_hill_climbing_result
        else result_value(result, "values")
    )

    figure = plt.figure(figsize=(12, 8))
    layout = figure.add_gridspec(2, 2, height_ratios=(1, 0.85))
    initial_axes = figure.add_subplot(layout[0, 0])
    final_axes = figure.add_subplot(layout[0, 1])
    objective_axes = figure.add_subplot(layout[1, :])

    draw_state(initial_axes, initial_state, vehicles, ship, "State Awal")
    draw_state(final_axes, final_state, vehicles, ship, "State Akhir")

    history = list(values)
    if history:
        first_iteration = 0 if is_hill_climbing_result else 1
        iterations = range(first_iteration, first_iteration + len(history))
        objective_axes.plot(
            iterations,
            history,
            color=OBJECTIVE_COLOR,
            linewidth=2,
            marker="o",
            markersize=3,
        )
    objective_axes.set_title("Nilai Objective Function per Iterasi")
    objective_axes.set_xlabel("Iterasi")
    objective_axes.set_ylabel("Nilai Objective Function")
    objective_axes.grid(color="#D7DCE2", linewidth=0.8, alpha=0.8)

    summary = [f"Objective akhir: {final_value}", f"Durasi: {duration:.4f} detik", *stats]
    figure.suptitle(title, fontsize=15, fontweight="bold")
    figure.text(0.5, 0.925, "  |  ".join(summary), ha="center", va="top", fontsize=9, wrap=True)
    figure.tight_layout(rect=(0, 0, 1, 0.89))
    return figure
