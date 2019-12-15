# Day 15: Oxygen System
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
FREE_SPACE = 1
OXYGEN = 2


def move_robot(robot, direction, reverse=False):
    reverse_directions = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
    next(robot)
    response = robot.send(direction if not reverse else reverse_directions[direction])
    if response not in (WALL, FREE_SPACE, OXYGEN):
        print("ERROR: Unexpected response: {}".format(response))
    return response


def direction_to_movement(direction):
    movement = {NORTH: (0, 1), SOUTH: (0, -1), EAST: (1, 0), WEST: (-1, 0)}
    return movement[direction]


def create_map(robot, area_map, position=(0, 0), cell_type=FREE_SPACE):
    area_map[position] = cell_type
    for direction in (NORTH, SOUTH, WEST, EAST):
        next_position = tuple(np.add(position, direction_to_movement(direction)))
        if next_position in area_map:
            continue
        response = move_robot(robot, direction)
        if response == WALL:
            continue
        create_map(robot, area_map, next_position, response)
        response = move_robot(robot, direction, reverse=True)


def bfs_flood_fill(start, area_map):
    visited = set()
    queue = [(start, 0)]
    distances = {}
    while len(queue) > 0:
        position, distance = queue.pop(0)
        if position not in area_map:
            continue
        if position in visited:
            continue
        distances[position] = distance
        visited.add(position)
        for direction in (NORTH, SOUTH, WEST, EAST):
            next_position = tuple(np.add(position, direction_to_movement(direction)))
            queue.append((next_position, distance + 1))
    return distances


def print_map(area_map):
    def get_positions_for_type(cell_type):
        x, y = zip(*[p for p, t in area_map.items() if t == cell_type])
        return x, y

    plt.plot(*get_positions_for_type(FREE_SPACE), 'bs', markersize=10)
    plt.plot(*get_positions_for_type(OXYGEN), 'rs', markersize=15)
    plt.show()


def part_one(area_map, oxygen_position):
    distances = bfs_flood_fill((0, 0), area_map)
    print("Shortest path to oxygen: {}".format(distances[oxygen_position]))


def part_two(area_map, oxygen_position):
    distances = bfs_flood_fill(oxygen_position, area_map)
    print("Time to fill space with oxygen: {}".format(max(distances.values())))


def main():
    program = intcom.get_program('15.txt')
    robot = intcom.run_program(program)
    area_map = {}
    create_map(robot, area_map, (0, 0))
    oxygen_position = next(position for position, cell_type in area_map.items() if cell_type == OXYGEN)
    print_map(area_map)
    part_one(area_map.copy(), oxygen_position)
    part_two(area_map.copy(), oxygen_position)


if __name__ == "__main__":
    main()
