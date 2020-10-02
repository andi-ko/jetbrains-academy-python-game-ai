# write your code here
import string

cells = []
width = 3
symbols = ["X", "O"]

while(True):
    initial_cells = input("Enter cells:")
    if len(initial_cells) != width**2:
        print("Illegal field!")
        continue
    if (initial_cells.count("X")
        + initial_cells.count("O")
        + initial_cells.count("_")
       != len(initial_cells)):
        print("Illegal characters provided!")
        continue
    if not 0 <= initial_cells.count("X") - initial_cells.count("O") <= 1:
        print("Only X may be one move ahead!")
        continue
    break

current_turn = initial_cells.count("X") + initial_cells.count("O")

for _i in range(3):
    cells.append([])

columns = iter(cells)

for index, value in enumerate(initial_cells):
    if index % width == 0:
        column = next(columns)
    column.append(value)


def is_finished():
    if current_turn == width**2:
        print("Draw")
        return True
    for column in cells:
        if all(cell == column[0] for cell in column) and column[0] in symbols:
            print(f"{column[0]} wins")
            return True
    transformed_cells = []
    for index in range(width):
        row = [column[index] for column in cells]
        if all(cell == row[0] for cell in row) and row[0] in symbols:
            print(f"{row[0]} wins")
            return True
    diagonal_1 = [cells[index][index] for index in range(width)]
    diagonal_2 = [cells[index][width - index - 1] for index in range(width)]
    if all(cell == diagonal_1[0] for cell in diagonal_1) and diagonal_1[0] in symbols:
        print(f"{diagonal_1[0]} wins")
        return True
    if all(cell == diagonal_2[0] for cell in diagonal_2) and diagonal_2[0] in symbols:
        print(f"{diagonal_2[0]} wins")
        return True

    print("Game not finished")
    return False


def draw_field(cells):
    print("---------")
    for column in cells:
        line = "| "
        for cell in column:
            line += cell + " "
        line += "|"
        print(line)
    print("---------")


draw_field(cells)


while True:
    string_input = input("Enter the coordinates:")

    if not string_input.find(" "):
        print("You should enter numbers!")
        continue
    string_coordinates = string_input.split(" ")

    if len(string_coordinates) != 2:
        print("You should enter numbers!")
        continue

    elif not all(string.digits.find(value) != -1 for value in string_coordinates):
        print("You should enter numbers!")
        continue

    string_coordinates.reverse()
    coordinates = [int(value) - 1 for value in string_coordinates]
    coordinates[0] = width - 1 - coordinates[0]

    if not all(0 <= value <= width - 1 for value in coordinates):
        print(f"Coordinates should be from 1 to {width}!")
        continue

    elif cells[coordinates[0]][coordinates[1]] != "_":
        print("This cell is occupied! Choose another one!")
        continue

    else:
        cells[coordinates[0]][coordinates[1]] = symbols[current_turn % 2]
        current_turn += 1
        draw_field(cells)
        if is_finished():
            break
        break
