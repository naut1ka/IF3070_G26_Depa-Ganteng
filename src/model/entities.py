from dataclasses import dataclass, replace
from typing import Optional, NamedTuple
from enum import Enum

class Dimensions(NamedTuple):
    w: int
    l: int

class Orientation(Enum):
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"

@dataclass(frozen=True)
class Placement:
    x: int
    y: int
    orientation: Orientation # x = kolom, y = baris, (x, y) = sudut kiri atas

@dataclass(frozen=True) 
class Vehicle:
    id: str
    shipping_fee: int
    weight: int
    eta: int
    dimensions: Dimensions # w = kolom, l = baris

    def effective_size(self, orientation):
        if orientation == Orientation.HORIZONTAL:  # HORIZONTAL = (w, l), VERTICAL = (l, w)
            return (self.dimensions.w, self.dimensions.l)
        return (self.dimensions.l, self.dimensions.w)

    def occupied_cells(self, placement: Placement) -> list[tuple[int,int]]:
        cols, rows = self.effective_size(placement.orientation)
        cells = []
        for dx in range(cols):
            for dy in range(rows):
                cells.append((placement.x + dx, placement.y + dy))
        return cells

@dataclass(frozen=True)
class Ship:
    State = dict[str, Optional[Placement]]
    dimensions: Dimensions # # w = kolom, l = baris
    max_capacity: int
    
        

# if __name__ == "__main__":
#     a = Vehicle(id="Dheva", shipping_fee=60, weight=6, eta=4, dimensions=Dimensions(w=1, l=2))
#     p = Placement(x=1, y=2, orientation=Orientation.HORIZONTAL)
#     p2 = replace(p, orientation=Orientation.VERTICAL)

#     cells = a.occupied_cells(p2)

#     assert set(cells) == {(1, 2), (2,2)}
#     print("lolos")