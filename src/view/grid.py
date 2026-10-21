
def show_grid(state, vehicles, ship):
    width = ship.dimensions.w
    length = ship.dimensions.l

    grid = []

    for y in range(length):
        row = []

        for x in range(width):
            row.append("")

        grid.append(row)

    for vehicle_id in state:
        posisi = state[vehicle_id]

        if posisi == None:
            continue

        vehicle = vehicles[vehicle_id]
        cells = vehicle.occupied_cells(posisi)

        for i in range(len(cells)):
            x = cells[i][0]
            y = cells[i][1]
            grid[y][x] = vehicle_id

    cell_width = 5

    for vehicle_id in vehicles:
        if len(vehicle_id) > cell_width:
            cell_width = len(vehicle_id)

    cell_width = cell_width + 2

    print()
    print("Kondisi Kapal")
    print("Ukuran:", width, "x", length)
    print()

    print("     ", end="")

    for x in range(width):
        print(str(x).center(cell_width), end="")

    print()

    for y in range(length):
        print("     ", end="")

        for x in range(width):
            print("+" + "-" * cell_width, end="")

        print("+")

        print(str(y).rjust(3), end="  ")

        for x in range(width):
            print("|" + grid[y][x].center(cell_width), end="")

        print("|")

    print("     ", end="")

    for x in range(width):
        print("+" + "-" * cell_width, end="")

    print("+")
    print()
