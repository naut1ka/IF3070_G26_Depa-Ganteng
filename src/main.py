from model.entities import Vehicle, Ship, Placement, Orientation, Dimensions
from model.neighbor import random_neighbor
from model.validation import is_valid

if __name__ == "__main__":
    ship = Ship(Dimensions(4, 2), 500)                       
    vehicles = [Vehicle(id="Dheva", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=2, l=2)), Vehicle(id="Afif", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=2, l=1)), Vehicle(id="Falzi", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=2, l=2))]
    state = {"Dheva": Placement(x=0, y=0, orientation=Orientation.HORIZONTAL), "Afif": Placement(x=2, y=0, orientation=Orientation.HORIZONTAL), "Falzi": None}
    before = dict(state)
    vehicles_by_id = {v.id: v for v in vehicles}

    for _ in range(50):
        new_state = random_neighbor(state, vehicles_by_id, ship)
        assert state == before

        jumlah_beda = sum(1 for k in state if state[k] != new_state[k])
        assert jumlah_beda == 1

        assert new_state["Falzi"] is None

        assert is_valid(state, vehicles_by_id, ship)

    print("rotate lolos")