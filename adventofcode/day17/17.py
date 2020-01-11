# Day 17: Set and Forget
import itertools as it
import os
import sys

import numpy as np
import scipy.ndimage as spimage

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


ASCII_SCAFFOLD = 35
ASCII_INTERSECTION = 88
ASCII_END = 43
ASCII_UP = 94
ASCII_DOWN = 118
ASCII_LEFT = 60
ASCII_RIGHT = 62


def get_image_from_robot(program):
    raw_pixels = [p for p in intcom.run_program(program)]
    ascii_image_data = [list(group) for k, group in it.groupby(raw_pixels, lambda x: x == 10) if not k]
    ascii_image = np.array(ascii_image_data)
    return ascii_image


def convert_image_to_binary(image, one_value):
    binary_imge = image == one_value
    return binary_imge.astype(int)


def find_intersections(binary_image):
    footprint = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]])
    intersections = spimage.minimum_filter(binary_image, footprint=footprint, mode='constant', cval=0)
    return intersections


def disp_image(ascii_image):
    for line in ascii_image:
        print(*(chr(p) for p in line))


def get_position_and_direction(ascii_image):
    ascii_to_direction = {ASCII_UP: [-1, 0], ASCII_DOWN: [1, 0], ASCII_LEFT: [0, -1], ASCII_RIGHT: [0, 1]}
    robot_position = np.where((ascii_image == ASCII_UP) | (ascii_image == ASCII_DOWN) | (ascii_image == ASCII_LEFT) | (ascii_image == ASCII_RIGHT))
    assert len(robot_position[0]) == 1
    assert len(robot_position[1]) == 1
    position = (robot_position[0][0], robot_position[1][0])
    direction = ascii_to_direction[ascii_image[position]]
    return np.array(position), np.array(direction)


def walk_scaffold(ascii_image, position, direction):
    def next_direction_generator(direction):
        direction = direction * np.array([-1, 1])
        direction[0], direction[1] = direction[1], direction[0]
        yield (direction, 'R')  # Right.
        yield (direction * -1, 'L')  # Left.

    def is_on_scaffold(position):
        try:
            return ascii_image[tuple(position)] == ASCII_SCAFFOLD
        except IndexError:
            return False

    path = []
    while True:
        # Find the next valid direction.
        for direction, symbol in next_direction_generator(direction):
            next_position = position + direction
            if is_on_scaffold(next_position):
                break
        else:
            # No valid direction found, the end scaffold is reached.
            break
        # Walk in the direction as long as possible.
        steps = 0
        while is_on_scaffold(next_position):
            position = next_position
            steps += 1
            next_position = position + direction
        path.append((symbol, steps))
    ascii_image[tuple(position)] = ASCII_END
    disp_image(ascii_image)
    print("Path:")
    print(",".join("{},{}".format(*e) for e in path))


def get_routines():
    # Created by hand using the result from the scaffold walk.
    main_routine = 'A,B,A,B,A,C,A,C,B,C\n'
    a_routine = 'R,6,L,10,R,10,R,10\n'
    b_routine = 'L,10,L,12,R,10\n'
    c_routine = 'R,6,L,12,L,10\n'
    video = 'n\n'  # Change to 'y' for a continuous video feed.
    return [main_routine, a_routine, b_routine, c_routine, video]


def part_one(program):
    ascii_image = get_image_from_robot(program)
    binary_image = convert_image_to_binary(ascii_image, ASCII_SCAFFOLD)
    intersections = find_intersections(binary_image)
    intersection_indexes = np.where(intersections == 1)
    ascii_image[intersection_indexes] = ASCII_INTERSECTION
    disp_image(ascii_image)
    calibration = sum(x * y for x, y in zip(intersection_indexes[0], intersection_indexes[1]))
    print("Camera calibration value: {}".format(calibration))


def part_two(program):
    ascii_image = get_image_from_robot(program.copy())
    position, direction = get_position_and_direction(ascii_image)
    walk_scaffold(ascii_image, position, direction)
    program[0] = 2  # Activate robot.
    output = intcom.run_ascii(program, get_routines())
    print("Collected space dust: {}".format(output))


def main():
    program = intcom.get_program('17.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
