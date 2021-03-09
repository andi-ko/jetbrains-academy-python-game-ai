# write your code here
import string
import random
import sys
import copy


def init_board(initial_cells=None):
    cells = []
    if not initial_cells:
        initial_cells = [" " for _i in range(width**2)]

    for _i in range(width):
        cells.append([])

    columns = iter(cells)

    for index, value in enumerate(initial_cells):
        if index % width == 0:
            column = next(columns)
        column.append(value)

    return cells


def enter_cells():
    global cells, current_turn

    while True:
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

    return initial_cells


def check_finished(state):
    if all(all(cell in symbols for cell in column) for column in state):
        return 2

    for column in state:
        if all(cell == column[0] for cell in column) and column[0] in symbols:
            if column[0] == symbols[0]:
                return 0
            else:
                return 1

    for index in range(width):
        row = [column[index] for column in state]
        if all(cell == row[0] for cell in row) and row[0] in symbols:
            if row[0] == symbols[0]:
                return 0
            else:
                return 1

    diagonal_1 = [state[index][index] for index in range(width)]
    diagonal_2 = [state[index][width - index - 1] for index in range(width)]

    if all(cell == diagonal_1[0] for cell in diagonal_1) and diagonal_1[0] in symbols:
        if diagonal_1[0] == symbols[0]:
            return 0
        else:
            return 1
    if all(cell == diagonal_2[0] for cell in diagonal_2) and diagonal_2[0] in symbols:
        if diagonal_2[0] == symbols[0]:
            return 0
        else:
            return 1

    return -1


def is_finished():
    global cells

    winner = check_finished(cells)
    if winner == 2:
        print("Draw")
        return True
    elif winner >= 0:
        print(f"{symbols[winner]} wins")
        return True
    # print("Game not finished")
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


def get_player_move():

    while True:
        string_input = input("Enter the coordinates:")

        if not string_input.find(" "):
            print("You should enter numbers!")
            continue
        string_coordinates = string_input.split()

        if len(string_coordinates) != 2:
            print("You should enter numbers!")
            continue

        elif any(string.digits.find(value) == -1 for value in string_coordinates):
            print("You should enter numbers!")
            continue

        # previous exercise version
        # string_coordinates.reverse()
        coordinates = [int(value) - 1 for value in string_coordinates]
        # previous exercise version
        # coordinates[0] = width - 1 - coordinates[0]

        if not all(0 <= value <= width - 1 for value in coordinates):
            print(f"Coordinates should be from 1 to {width}!")
            continue

        elif cells[coordinates[0]][coordinates[1]] in symbols:
            print("This cell is occupied! Choose another one!")
            continue

        return coordinates


def get_easy_ai_move():
    global cells

    x = random.randint(0, width - 1)
    y = random.randint(0, width - 1)
    while cells[x][y] in symbols:
        x = random.randint(0, width - 1)
        y = random.randint(0, width - 1)

    return [x, y]


def get_medium_ai_move():
    global cells
    global current_turn

    ai_symbol = symbols[current_turn % 2]
    opponent_symbol = symbols[(current_turn + 1) % 2]

    # check if winning move is possible

    for column_id, column in enumerate(cells):
        if column.count(ai_symbol) == width - 1:
            if column.count(" ") and column.index(" "):
                return [column_id, column.index(" ")]

    for index in range(width):
        row = [column[index] for column in cells]
        for row_id, row in enumerate(row):
            if row.count(ai_symbol) == width - 1:
                if row.index(" "):
                    return [row.index(" "), row_id]

    diagonal_1 = [cells[index][index] for index in range(width)]
    diagonal_2 = [cells[index][width - index - 1] for index in range(width)]
    if diagonal_1.count(ai_symbol) == width - 1:
        if diagonal_1.count(" ") and diagonal_1.index(" "):
            return [diagonal_1.index(" "), diagonal_1.index(" ")]
    if diagonal_2.count(ai_symbol) == width - 1:
        if diagonal_2.count(" ") and diagonal_2.index(" "):
            return [diagonal_2.index(" "), width - diagonal_2.index(" ") - 1]

    # check if blocking winning move is possible

    for column_id, column in enumerate(cells):
        if column.count(opponent_symbol) == width - 1:
            if column.count(" ") and column.index(" "):
                return [column_id, column.index(" ")]

    for index in range(width):
        row = [column[index] for column in cells]
        for row_id, row in enumerate(row):
            if row.count(opponent_symbol) == width - 1:
                if row.count(" ") and row.index(" "):
                    return [row.index(" "), row_id]

    diagonal_1 = [cells[index][index] for index in range(width)]
    diagonal_2 = [cells[index][width - index - 1] for index in range(width)]
    if diagonal_1.count(opponent_symbol) == width - 1:
        if diagonal_1.count(" ") and diagonal_1.index(" "):
            return [diagonal_1.index(" "), diagonal_1.index(" ")]
    if diagonal_2.count(opponent_symbol) == width - 1:
        if diagonal_2.count(" ") and diagonal_2.index(" "):
            return [diagonal_2.index(" "), width - diagonal_2.index(" ") - 1]

    return get_easy_ai_move()


def minimax(state, turn, opponents_turn):

    # check if game over
    winner = check_finished(state)

    if winner in [0, 1]:
        if opponents_turn:
            return [None, 1]
        else:
            return [None, -1]
    if winner == 2:
        return [None, 0]

    moves = []
    for column_id, column in enumerate(state):
        for cell_id, cell in enumerate(column):
            if cell not in symbols:
                moves.append([column_id, cell_id])

    if opponents_turn:
        best_move = [None, 2]
    else:
        best_move = [None, -2]

    for move in moves:
        new_state = copy.deepcopy(state)
        new_state[move[0]][move[1]] = symbols[turn % 2]

        # else run minimax
        this_move = minimax(new_state, turn + 1, not opponents_turn)

        if opponents_turn:
            if this_move[1] < best_move[1]:
                best_move[0] = move
                best_move[1] = this_move[1]
        else:
            if this_move[1] > best_move[1]:
                best_move[0] = move
                best_move[1] = this_move[1]

    return best_move


def get_hard_ai_move():
    global cells

    return minimax(copy.deepcopy(cells), current_turn, False)[0]


def set_players(players):
    global is_ai, ai_level

    for player_id, player in enumerate(players):
        if player == "user":
            is_ai[player_id] = False
        elif player in ai_levels:
            is_ai[player_id] = True
            ai_level[player_id] = player
        else:
            return False

    return True


def set_game_mode():

    while True:
        string_input = input("Input command:")

        if string_input.startswith("exit"):
            return False

        if not string_input.find(" "):
            print("Bad parameters!")
            continue
        parameters = string_input.split(" ")

        if len(parameters) != 3:
            print("Bad parameters!")
            continue

        if parameters[0] == "start":
            if not set_players(parameters[1:3]):
                print("Bad parameters!")
                continue
            else:
                return True


def run_game():
    global current_turn

    while True:
        if is_ai[current_turn % 2]:
            if ai_level[current_turn % 2] == "easy":
                coordinates = get_easy_ai_move()
            elif ai_level[current_turn % 2] == "medium":
                coordinates = get_medium_ai_move()
            elif ai_level[current_turn % 2] == "hard":
                coordinates = get_hard_ai_move()
            print ('Making move level "' + ai_level[current_turn % 2] + '"')
        else:
            if current_turn == 0:
                draw_field(cells)
            coordinates = get_player_move()

        cells[coordinates[0]][coordinates[1]] = symbols[current_turn % 2]
        draw_field(cells)
        if is_finished():
            break
        current_turn += 1


width = 3
symbols = ["X", "O"]
current_turn = 0
is_ai = [False, False]
ai_levels = ["easy", "medium", "hard"]
ai_level = ['"easy"', "'easy'"]

# set_board(enter_cells())
cells = init_board(None)

# draw_field(cells)

while True:
    if set_game_mode():
        run_game()
    else:
        break



