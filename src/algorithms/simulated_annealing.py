import math
import random
import time
from dataclasses import dataclass
from model.entities import Vehicle, Ship, Orientation, State
from model.initial import initial_state
from model.neighbor import rotate, move, swap
from model.validation import is_valid
from model.objective import value

@dataclass
class SAResult:
    initial_state: State
    final_state: State
    final_value: int
    values: list[int]           
    probabilities: list[float]   
    stuck_count: int
    iterations: int
    duration: float #dalam detik

def acceptance_probability(delta: float, temperature: float) -> float:
    if delta >= 0:
        return 1.0
    return math.exp(delta / temperature)

def random_candidate(state, vehicles, ship, attempts=20): #note: ini masih belum pasti attempts jadi inputan atau udah distate
    carried = []

    for vehicle_id, placement in state.items():

        if placement is not None:
            carried.append(vehicle_id)

    if carried == []:
        return None


    for _ in range(attempts):
        kind = random.choice(["rotate", "move", "swap"])

        if kind == "rotate":
            candidate = rotate(state, random.choice(carried))

        if kind == "move":
            vehicle_id = random.choice(list(state))
            placement = state[vehicle_id]

            if placement is None:
                orientation = random.choice(list(Orientation))
            else:
                orientation = placement.orientation
                
            vehicle = vehicles[vehicle_id]
            cols, rows = vehicle.effective_size(orientation)
                            
            max_x = ship.dimensions.w - cols
            max_y = ship.dimensions.l - rows

            if max_x < 0 or max_y < 0:
                    continue
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            
            candidate = move(state, vehicle_id, x, y, orientation)

        if kind == "swap":
            a = random.choice(carried)
            others = [n for n in state if n != a]

            if others == []:
                 continue
            
            b = random.choice(others)

            candidate = swap(state, a, b)

        if is_valid(candidate, vehicles, ship):
            return candidate
    return None

def simulated_annealing(vehicles, ship, initial_temp: float, alpha, max_iteration, seed, min_temp=1e-9, stuck_limit = 50) -> SAResult: #note: stuck_limit juga masih belum pasti berapa tergantung besar datanya

    if initial_temp <= 0 or not (0 < alpha < 1):
        raise ValueError("initial temp atau alpha tidak valid")

    random.seed(seed)

    t0 = time.perf_counter()
    state = initial_state(vehicles, ship)
    start = state
    current = value(state, vehicles)
    T = initial_temp
    i = 0
    values = []
    probabilities = []
    streak = 0
    stuck_count = 0

    while T > min_temp and i < max_iteration:
        before = current
        candidate = random_candidate(state, vehicles, ship)
        p = 0.0

        if candidate is not None:
            candidate_value = value(candidate, vehicles)
            delta = candidate_value - current
            p = acceptance_probability(delta, T)
            
            if p > random.random():
                current = candidate_value
                state = candidate

        values.append(current)
        probabilities.append(p)

        if current != before:
            streak = 0
        if(before == current):
            streak += 1

        if streak == stuck_limit:
            stuck_count += 1

        T = T * alpha
        i += 1

    return SAResult(start, state, current, values, probabilities, stuck_count, i, duration= time.perf_counter() - t0)