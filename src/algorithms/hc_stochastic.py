
import random

from model.initial import initial_state
from model.neighbor import move, swap
from model.validation import is_valid
from model.objective import value
from model.entities import Placement, Orientation


def find_better_neighbors(current_state, vehicles, ship):
    current_value = value(current_state, vehicles)
    better_neighbors = []

    for v_id in vehicles:
        vehicle = vehicles[v_id]
        posisi = current_state[v_id]

        if posisi is None:
            for orient in Orientation:
                cols, rows = vehicle.effective_size(orient)

                for y in range(ship.dimensions.l - rows + 1):
                    for x in range(ship.dimensions.w - cols + 1):
                        new_state = dict(current_state)
                        new_state[v_id] = Placement(x, y, orient)

                        if is_valid(new_state, vehicles, ship):
                            new_value = value(new_state, vehicles)

                            if new_value > current_value:
                                better_neighbors.append(new_state)

        else:
            for orient in Orientation:
                new_state = dict(current_state)
                new_state[v_id] = Placement(
                    posisi.x, posisi.y, orient
                )

                if is_valid(new_state, vehicles, ship):
                    new_value = value(new_state, vehicles)

                    if new_value > current_value:
                        better_neighbors.append(new_state)


            for y in range(ship.dimensions.l):
                for x in range(ship.dimensions.w):
                    new_state = move(current_state, v_id, x, y)

                    if is_valid(new_state, vehicles, ship):
                        new_value = value(new_state, vehicles)

                        if new_value > current_value:
                            better_neighbors.append(new_state)


    vehicle_ids = list(vehicles.keys())

    for i in range(len(vehicle_ids)):
        for j in range(i + 1, len(vehicle_ids)):
            new_state = swap(
                current_state,
                vehicle_ids[i],
                vehicle_ids[j]
            )

            if is_valid(new_state, vehicles, ship):
                new_value = value(new_state, vehicles)

                if new_value > current_value:
                    better_neighbors.append(new_state)

    return better_neighbors


def stochastic_hill_climbing(vehicles, ship):
    current_state= initial_state(vehicles,ship)
    start_state = dict(current_state)
    iterations = 0
    
    while True:
        better_neighbors = find_better_neighbors(current_state, vehicles, ship)
        
        if not better_neighbors:
            break
        
        current_state = random.choice(better_neighbors)
        iterations +=1 
    
    final_state = current_state 
    final_value = value(final_state, vehicles)
    
    return{
        "initial_state" : start_state,
        "final_state" : final_state,
        "final_value" : final_value,
        "iterations" : iterations
    } 

