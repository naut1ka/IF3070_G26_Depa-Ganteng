import random
import time
from dataclasses import dataclass
from model.entities import Vehicle, Ship, State
from model.initial import initial_state
from model.neighbor import rotate, move, swap
from model.validation import is_valid
from model.objective import value

@dataclass
class GAResult:
    initial_state: State
    final_state: State
    final_value: int
    values: list[int]
    mean_values: list[float]
    iterations: int
    duration: float
    population_size: int

def evaluate_fitness(state: State, vehicles: dict, ship: Ship) -> int:
    candidate = state
    if is_valid(candidate, vehicles, ship):
        return value(candidate, vehicles)
    return 0

def roulette_wheel_selection(population: list[State], fitness_list: list[int]) -> State:
    total_fitness = sum(fitness_list)
    if total_fitness == 0:
        return population[random.randint(0, len(population) - 1)]

    pick = random.uniform(0, total_fitness)
    current = 0.0

    for i in range (len(population)):
        current = current + fitness_list[i]
        if (current >= pick):
            return population[i]

    return population[-1]

def sus_selection(population: list[State], fitness_list: list[int], n_parents: int = 2) -> list[State]:
    total_fitness=sum(fitness_list)
    if total_fitness == 0:
        return [population[random.randint(0, len(population))] for _ in range(n_parents)]

    distance = total_fitness/n_parents
    start = random.uniform(0, distance)
    pointers = [start + i * distance for i in range(n_parents)]

    selected_parents = []
    for point in pointers:
        i = 0
        current = fitness_list[0]
        while current < point and i < len(population)-1:
            i+=1
            current+=fitness_list[i]
        selected_parents.append(population[i])

    return selected_parents

def rank_selection(population: list[State], fitness_list: list[int]) -> State:

    n = len(population)
    if n == 0 or n != len(fitness_list):
        raise ValueError("populasi kosong atau panjang tidak sama dengan fitness")
    if n == 1:
        return population[0]
    s = 1.5 
    order = sorted(range(n), key=lambda i: fitness_list[i])
    weights = [0.0] * n
    for r, i in enumerate(order): # r ini rank/position per i
        weights[i] = (2 - s) + 2 * (s - 1) * r / (n - 1)
    return random.choices(population, weights=weights, k=1)[0]

def tournament_selection(population: list[State], fitness_list: list[int], k: int) -> State:
    candidate_index = random.sample(range(len(population)),k)
    best_index = candidate_index[0]

    for i in candidate_index:
        if fitness_list[i] > fitness_list[best_index]:
            best_index=i
    return population[best_index]

def crossover(parent_a: State, parent_b: State, vehicles: dict) -> State:
    vehicles_ids = list(vehicles.keys())
    gene_length = len(vehicles_ids)

    if gene_length <= 1:
        return parent_a.copy()

    cutting_point = random.randint(1, gene_length-1)

    child = dict()
    for i in range (0, cutting_point):
        vehicle_id = vehicles_ids[i]
        child[vehicle_id] = parent_a[vehicle_id]

    for i in range (cutting_point, gene_length):
        vehicle_id = vehicles_ids[i]
        child[vehicle_id] = parent_b[vehicle_id]

    return child

        
def mutate_candidate(state: State, vehicles: dict, ship: Ship):
    carried = []
    for vehicle_id, placement in state.items():
        if placement is not None:
            carried.append(vehicle_id)

    if carried == []:
        return None

    kind = random.choice(["rotate","move","swap"])

    if kind == "rotate":
        vehicle_id = random.choice(carried)
        return rotate(state, vehicle_id)

    elif kind == "move":
        vehicle_id = random.choice(carried)
        placement = state[vehicle_id]
        vehicle = vehicles[vehicle_id]
        cols, rows = vehicle.effective_size(placement.orientation)

        max_x = ship.dimensions.w - cols
        max_y = ship.dimensions.l - rows
        if max_x < 0 or max_y < 0:
            return None
        
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        return move(state, vehicle_id, x, y)

    elif kind == "swap":
        state_a = random.choice(carried)
        others = [n for n in state if n != state_a]
        if others == []:
            return None
        
        state_b = random.choice(others)
        return swap(state, state_a, state_b)

def genetic_algorithm(vehicles: dict, ship: Ship, pop_size: int, max_generations: int, p_mutation: float, seed: float, elite_size: int = 2, k: int = 3) -> GAResult:

    random.seed(seed)
    t0 = time.perf_counter()

    population = []
    for i in range(pop_size):
        state = initial_state(vehicles, ship)
        population.append(state)

    fitness_list = [evaluate_fitness(individual_state, vehicles, ship) for individual_state in population]
    best_idx = fitness_list.index(max(fitness_list))

    initial_best_state = population[best_idx]
    best_overall_state = population[best_idx]
    best_overall_value = fitness_list[best_idx]

    max_values = []
    mean_values = []

    # loop sesuai jumlah iterasi (disini akan disebut generasi, 1 iterasi = 1 generasi, biar kayak genetic banget)
    for gen in range (max_generations):
        fitness_list = [evaluate_fitness(individual_state, vehicles, ship) for individual_state in population]
        current_max = max(fitness_list)
        current_mean = sum(fitness_list) / len(fitness_list)

        max_values.append(current_max)
        mean_values.append(current_mean)

        best_idx = fitness_list.index(current_max)

        if current_max > best_overall_value:
            best_overall_value = current_max
            best_overall_state = population[best_idx]

        new_population = []
        sorted_population = [state for _, state in sorted(zip(fitness_list, population), key=lambda x: x[0],reverse=True)]

        for z in range (0,elite_size): 
            new_population.append(sorted_population[z])

        while len(new_population) < pop_size:
            # Tournament Selection
            parent_a = tournament_selection(population, fitness_list, k)
            parent_b = tournament_selection(population, fitness_list, k)

            # Roulette Wheel Selection
            # parent_a = roulette_wheel_selection(population, fitness_list)
            # parent_b = roulette_wheel_selection(population, fitness_list)

            # SUS Selection
            # parent_a = sus_selection(population, fitness_list)[0]
            # parent_b = sus_selection(population, fitness_list)[1]

            # # Rank Selection
            # parent_a = rank_selection(population, fitness_list)
            # parent_b = rank_selection(population, fitness_list)

            child = crossover(parent_a, parent_b, vehicles)
            
            if random.uniform(0,1) < p_mutation:
                mutated = mutate_candidate(child, vehicles, ship)
                if mutated is not None:
                    child = mutated

            new_population.append(child)

        population = new_population

    duration = time.perf_counter() - t0
    return GAResult(
        initial_state=initial_best_state,
        final_state=best_overall_state,
        final_value=best_overall_value,
        values=max_values,
        mean_values=mean_values,
        iterations=len(max_values),
        duration=duration,
        population_size=pop_size
    )