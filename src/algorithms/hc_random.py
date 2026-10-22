import time
from algorithms.hc_steepest import steepest_ascent


def random_restart(vehicles, ship, max_restarts:int):
    start_time = time.perf_counter()

    best_result = None
    best_value = -1

    restart_count = 0
    iterations_per_restart = []
    history = []

    for i in range(max_restarts):
        result = steepest_ascent(vehicles, ship)

        current_value = result["final_value"]

        restart_count += 1
        iterations_per_restart.append(result["iterations"])
        history.extend(result["history"])

        if current_value > best_value:
            best_result = result
            best_value = current_value
    duration = time.perf_counter() - start_time
    
    return{
        "initial_state": best_result["initial_state"],
        "final_state": best_result["final_state"],
        "final_value": best_result["final_value"],
        "iterations": best_result["iterations"],
        "restart_count": restart_count,
        "iterations_per_restart": iterations_per_restart,
        "history" : history,
        "duration" : duration
    }