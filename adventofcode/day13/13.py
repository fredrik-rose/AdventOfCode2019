# Day 13: Care Package
import collections as coll
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


EMPTY_TILE = 0
WALL_TILE = 1
BLOCK_TILE = 2
PADDLE_TILE = 3
BALL_TILE = 4
DISPLAY = (-1, 0)


def plot_tiles(tiles):
    colors = {WALL_TILE: 'k', BLOCK_TILE: 'g', PADDLE_TILE: 'b', BALL_TILE: 'r'}
    for tile_type, color in colors.items():
        positions = [position for position, tile in tiles.items() if tile == tile_type]
        x = [position[0] for position in positions]
        y = [-position[1] for position in positions]
        plt.plot(x, y, 's' + color, markersize=10)
    plt.show()


def part_one(program):
    game = intcom.run_program(program)
    tiles = coll.defaultdict(int)
    for x, y, tile in zip(game, game, game):
        tiles[(x, y)] = tile
    number_of_block_tiles = sum(1 if tile == BLOCK_TILE else 0 for tile in tiles.values())
    plot_tiles(tiles)
    print("Number of blocks: {}".format(number_of_block_tiles))


def part_two(program):
    def get_position(tile_type):
        for position, tile in tiles.items():
            if tile == tile_type:
                return position

    def request_input():
        paddle = get_position(PADDLE_TILE)
        ball = get_position(BALL_TILE)
        # plot_tiles(tiles)
        return np.sign(ball[0] - paddle[0])

    program[0] = 2
    game = intcom.run_program(program, request_input)
    tiles = coll.defaultdict(int)
    for x, y, tile in zip(game, game, game):
        if (x, y) == DISPLAY:
            score = tile
        else:
            tiles[(x, y)] = tile
    plot_tiles(tiles)
    print("Score: {}".format(score))


def main():
    program = intcom.get_program('13.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
