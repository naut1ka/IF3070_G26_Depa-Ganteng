from model.entities import Vehicle, Ship, Placement, Orientation, Dimensions
from model.neighbor import rotate
from model.validation import is_valid
from model.initial import initial_state
from algorithms.simulated_annealing import random_candidate, simulated_annealing, value
import random

if __name__ == "__main__":
    random.seed(1)
    ship = Ship(Dimensions(4, 2), 500)                       
    vehicles = [Vehicle(id="Dheva", shipping_fee=30, weight=6, eta=4, dimensions=Dimensions(w=2, l=2)), Vehicle(id="Afif", shipping_fee=10, weight=6, eta=4, dimensions=Dimensions(w=2, l=1)), Vehicle(id="Falzi", shipping_fee=25, weight=6, eta=4, dimensions=Dimensions(w=2, l=2))]

    vehicles_by_id = {v.id: v for v in vehicles}

    result = simulated_annealing(vehicles_by_id, ship, 100, 0.995, 50000, 1)
    print (result.final_value, result.stuck_count, result.iterations, result.duration, result.values[0], min(result.values), max(result.values))

    random.seed(1); a = initial_state(vehicles_by_id, ship)
    random.seed(1); b = initial_state(vehicles_by_id, ship)
    random.seed(2); c = initial_state(vehicles_by_id, ship)

    print(a, b, c)