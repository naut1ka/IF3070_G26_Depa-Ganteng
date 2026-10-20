from model.entities import Vehicle, Ship, Placement, Orientation, Dimensions
from model.neighbor import rotate
from model.validation import is_valid
from model.initial import initial_state

if __name__ == "__main__":
    ship = Ship(Dimensions(4, 2), 500)                       
    vehicles = [Vehicle(id="Dheva", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=2, l=2)), Vehicle(id="Afif", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=2, l=1)), Vehicle(id="Falzi", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=2, l=2))]
    state = {"Dheva": Placement(x=0, y=0, orientation=Orientation.HORIZONTAL), "Afif": Placement(x=2, y=0, orientation=Orientation.HORIZONTAL), "Falzi": None}
    before = dict(state)
    vehicles_by_id = {v.id: v for v in vehicles}


    print(initial_state(vehicles_by_id, ship))