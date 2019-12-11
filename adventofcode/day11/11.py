# Day 11: Space Police
import collections as coll
import os
import sys

import numpy as np
import PIL.Image as pimage

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


BLACK = 0
WHITE = 1
LEFT_90_DEGREES = 0
RIGHT_90_DEGREES = 1


def rotate(direction, rotation):
    rotations = {LEFT_90_DEGREES: lambda x: (-x[1], x[0]),
                 RIGHT_90_DEGREES: lambda x: (x[1], -x[0])}
    return rotations[rotation](direction)


def run_painting_robot(program, start_color=BLACK):
    robot = intcom.run_program(program)
    position = (0, 0)
    direction = (0, 1)
    panels = coll.defaultdict(lambda: BLACK)
    panels[position] = start_color
    while True:
        try:
            next(robot)
            panels[position] = robot.send(panels[position])
            direction = rotate(direction, next(robot))
            position = tuple(np.add(position, direction))
        except StopIteration:
            return panels


def plot_panels(panels):
    x, y = zip(*panels.keys())
    panels = {(p[0] - min(x), p[1] - min(y)): c for p, c in panels.items()}
    image_size = (max(panels.keys(), key=lambda x: x[0])[0] + 1,
                  max(panels.keys(), key=lambda x: x[1])[1] + 1)
    image = pimage.new('1', image_size)
    for position, color in panels.items():
        image.putpixel(position, color)
    image = image.resize((image.width * 10, image.height * 10))
    image.transpose(pimage.FLIP_TOP_BOTTOM).show()


def part_one(program):
    panels = run_painting_robot(program)
    plot_panels(panels)
    print("Number of panels painted at least once: {}".format(len(panels)))


def part_two(program):
    panels = run_painting_robot(program, WHITE)
    plot_panels(panels)


def main():
    program = intcom.get_program('11.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
