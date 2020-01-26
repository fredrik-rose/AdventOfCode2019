# Day 24: Planet of Discord
import math

import numpy as np
import scipy.ndimage.filters as filters


BUG = '#'
EMPTY_SPACE = '.'


def parse_input(file_path):
    with open(file_path) as file:
        raw_data = [list(line) for line in file.read().splitlines()]
        char_array = np.array(raw_data)
        board = np.zeros(char_array.shape, dtype=np.int8)
        board[char_array == BUG] = 1
    return board


def create_rules():
    def rules(cells):
        my_cell = cells[index_of_my_position]
        number_of_bugs = sum(cells)
        if my_cell == 1:
            return 1 if number_of_bugs == 2 else 0
        else:
            return 1 if number_of_bugs == 1 or number_of_bugs == 2 else 0

    footprint = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]])
    index_of_my_position = 2
    return rules, footprint


def simulate_game_of_life(board, rules, footprint):
    return filters.generic_filter(board, rules, footprint=footprint, mode='constant', cval=0)


def simulate_recursive_game_of_life(board):
    # TODO: This function is (obviously) a mess and needs a cleanup.
    new_board = np.copy(board)
    # The center cell is a recursion down to the lower level.
    recursion_cell = (board.shape[1] // 2, board.shape[2] // 2)
    for current_level, current_y, current_x in np.ndindex(*board.shape):
        if (current_y, current_x) == recursion_cell:
            # The center cell is a recursion down to the lower level.
            continue
        neighbours = []
        for y_offset, x_offset in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            y = current_y + y_offset
            x = current_x + x_offset
            upper_level_available = current_level + 1 < board.shape[0]
            lower_level_available = current_level - 1 >= 0
            # Check if the position is outside the board. If so, get bugs from the upper level.
            if y < 0:
                if upper_level_available:
                    neighbours.append(board[current_level + 1, recursion_cell[0] - 1, recursion_cell[1]])
            elif y >= board.shape[1]:
                if upper_level_available:
                    neighbours.append(board[current_level + 1, recursion_cell[0] + 1, recursion_cell[1]])
            elif x < 0:
                if upper_level_available:
                    neighbours.append(board[current_level + 1, recursion_cell[0], recursion_cell[1] - 1])
            elif x >= board.shape[2]:
                if upper_level_available:
                    neighbours.append(board[current_level + 1, recursion_cell[0], recursion_cell[1] + 1])
            # Check if the position is the recursion cell. If so, get bugs from the lower level.
            elif (y, x) == recursion_cell:
                if lower_level_available:
                    if y_offset == -1:
                        neighbours += list(board[current_level - 1, board.shape[1] - 1, :])
                    elif y_offset == 1:
                        neighbours += list(board[current_level - 1, 0, :])
                    elif x_offset == -1:
                        neighbours += list(board[current_level - 1, :, board.shape[2] - 1])
                    elif x_offset == 1:
                        neighbours += list(board[current_level - 1, :, 0])
            # Get bugs from the neighbor cells.
            else:
                neighbours.append(board[current_level, y, x])
        # Update the board according to the rules of the game.
        number_of_bugs = sum(neighbours)
        if board[current_level, current_y, current_x] == 1:
            new_board[current_level, current_y, current_x] = 1 if number_of_bugs == 1 else 0
        else:
            new_board[current_level, current_y, current_x] = 1 if number_of_bugs == 1 or number_of_bugs == 2 else 0
    return new_board


def calculate_biodiversity_rating(board):
    biodiversity_rating = 0
    for i, cell in enumerate(np.nditer(board)):
        if cell == 1:
            biodiversity_rating += int(math.pow(2, i))
    return biodiversity_rating


def part_one(board):
    rules, footprint = create_rules()
    seen_boards = set()
    while True:
        board_hash = hash(str(board))
        if board_hash in seen_boards:
            biodiversity_rating = calculate_biodiversity_rating(board)
            print("Biodiversity rating for the first layout that appears twice: {}".format(biodiversity_rating))
            break
        seen_boards.add(board_hash)
        board = simulate_game_of_life(board, rules, footprint)


def part_two(board):
    zeroes = np.zeros((1, *board.shape))
    board = board.reshape(1, *board.shape)
    for _ in range(200):
        board = np.concatenate((np.copy(zeroes), board, np.copy(zeroes)))
        board = simulate_recursive_game_of_life(board)
    number_of_bugs = int(np.sum(board))
    print("Number of bugs: {}".format(number_of_bugs))


def main():
    board = parse_input('24.txt')
    part_one(np.copy(board))
    part_two(np.copy(board))


if __name__ == "__main__":
    main()
