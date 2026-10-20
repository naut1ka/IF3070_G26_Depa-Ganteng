from dataclasses import replace
from model.entities import Vehicle, Ship, Placement, Orientation, State, Dimensions

def flip(orientation: Orientation) -> Orientation:
    if orientation == Orientation.HORIZONTAL:
        return Orientation.VERTICAL
    return Orientation.HORIZONTAL

def rotate(state: State, vehicle_id: str) -> State:
    new_state = dict(state)
    old = state[vehicle_id]
    if old is None:
        return dict(state)
    new_state[vehicle_id] = replace (old, orientation = flip(old.orientation))
    return new_state

# if __name__ == "__main__":
#     ship = Ship(Dimensions(4, 2), 500)                       
#     vehicles = [Vehicle(id="Dheva", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=1, l=2)), Vehicle(id="Afif", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=1, l=3)), Vehicle(id="Falzi", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=2, l=2))]
#     state = {"Dheva": Placement(x=1, y=2, orientation=Orientation.HORIZONTAL), "Afif": Placement(x=1, y=2, orientation=Orientation.HORIZONTAL), "Falzi": None}
#     before = dict(state)

#     for _ in range(50):
#         new_state = random_neighbor(state, vehicles, ship)
#         assert state == before

#         jumlah_beda = sum(1 for k in state if state[k] != new_state[k])
#         assert jumlah_beda == 1

#         assert new_state["Falzi"] is None

#     print("rotate lolos")