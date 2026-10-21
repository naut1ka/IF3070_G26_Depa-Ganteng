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
    probabilities: list[float]   
    stuck_count: int
    iterations: int
    duration: float #dalam detik

def evaluate_fitness(state: State, vehicles: dict, ship: Ship) -> int:
    candidate = state
    if is_valid(candidate, vehicles, ship):
        return value(candidate, vehicles)
    return 0

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

def genetic_algorithm(vehicles: dict, ship: Ship, pop_size: int, max_generations: int, p_mutation: float, seed: int, elite_size: int = 1, k: int = 3, stuck_limit: int = 50) -> GAResult:

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
    streak = 0
    stuck_count = 0

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
            streak = 0
        else:
            streak += 1
            if streak == stuck_limit:
                stuck_count += 1
                streak = 0

        new_population = []
        sorted_population = [state for _, state in sorted(zip(fitness_list, population), key=lambda x: x[0],reverse=True)]

        for z in range (0,elite_size): 
            new_population.append(sorted_population[z])

        while len(new_population) < pop_size:
            parent_a = tournament_selection(population, fitness_list, k)
            parent_b = tournament_selection(population, fitness_list, k)

            child = crossover(parent_a, parent_b, vehicles)
            
            if random.uniform(0,1) < p_mutation:
                mutated = mutate_candidate(child, vehicles, ship)
                if mutated is not None:
                    child = mutated

            new_population.append(child)

        population = new_population

    duration = time.perf_counter() - t0
    total_fitness = sum(fitness_list)
    probabilities = (
        [fitness / total_fitness for fitness in fitness_list]
        if total_fitness > 0
        else [1 / len(fitness_list)] * len(fitness_list)
    )

    return GAResult(initial_best_state,best_overall_state, best_overall_value, max_values, probabilities, stuck_count, len(max_values), duration)