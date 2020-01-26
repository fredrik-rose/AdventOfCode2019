# Day 25: Cryostasis
import itertools as itools
import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


MANUAL_PLAY = False


def manual_input_generator():
    while True:
        command = input('> ')
        yield '{}\n'.format(command)


def automatic_input_generator():
    # Commands to pick up all (good) items. Created by manually playing the game.
    commands = (
        'west\n',
        'take cake\n',
        'west\n',
        'take pointer\n',
        'south\n',
        'take monolith\n',
        'north\n',
        'west\n',
        'south\n',
        'take tambourine\n',
        'east\n',
        'east\n',
        'east\n',
        'take mug\n',
        'west\n',
        'west\n',
        'west\n',
        'north\n',
        'east\n',
        'east\n',
        'east\n'
        'south\n',
        'take coin\n',
        'east\n',
        'take mouse\n',
        'south\n',
        'south\n',
        'take hypercube\n',
        'north\n',
        'north\n',
        'west\n',
        'south\n',
        'west\n',
        'north\n',
        'north\n',
        'inv\n')
    for cmd in commands:
        yield cmd
    # Brute force to find the correct combination of items to get through the door.
    items = ('pointer', 'hypercube', 'cake', 'tambourine', 'monolith', 'mouse', 'coin', 'mug')
    for combination in generate_all_combinations(items):
        for item in items:
            yield 'drop {}\n'.format(item)
        for item in combination:
            yield 'take {}\n'.format(item)
        yield 'north\n'


def generate_all_combinations(items):
    for i in range(len(items)):
        for combination in itools.combinations(items, i + 1):
            yield combination


def part_one(program):
    input_generator = manual_input_generator() if MANUAL_PLAY else automatic_input_generator()
    intcom.run_ascii(program, input_generator)


def main():
    program = intcom.get_program('25.txt')
    part_one(program.copy())


if __name__ == "__main__":
    main()
