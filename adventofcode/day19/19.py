# Day 19: Tractor Beam
import os
import sys

import matplotlib.pyplot as plt

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


def scan_position(program, x, y):
    drone = intcom.run_program(program.copy())
    next(drone)
    drone.send(x)
    return drone.send(y)


def visualize_tractor_beam(space_map):
    x, y = zip(*space_map)
    plt.plot(x, y, 's')
    plt.show()


def part_one(program):
    space_map = set()
    for y in range(0, 50):
        for x in range(0, 50):
            drone = intcom.run_program(program.copy())
            next(drone)
            drone.send(x)
            output = drone.send(y)
            if output == 1:
                space_map.add((x, y))
    print("Part one: {}".format(len(space_map)), flush=True)
    visualize_tractor_beam(space_map)


def part_two(program):
    ship_size = 100
    search_region = 10000
    left = 0
    for y in range(ship_size, search_region):
        for x in range(left, search_region):
            point = scan_position(program, x, y)
            if point == 1:
                left = x
                # Check if the ship fits inside the tractor beam.
                offset = ship_size - 1
                point = scan_position(program, x + offset, y - offset)
                if point == 1:
                    print("Part two: {}".format(x * 10000 + (y - offset)), flush=True)
                    return
                break


def main():
    program = intcom.get_program('19.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
