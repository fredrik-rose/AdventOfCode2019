# Day 5: Sunny with a Chance of Asteroids
import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


def part_one(program):
    print("Part one")
    computer = intcom.run_program(program)
    next(computer)
    print(computer.send(1))
    for output in computer:
        print(output)


def part_two(program):
    print("Part two")
    computer = intcom.run_program(program)
    next(computer)
    print(computer.send(5))


def main():
    program = intcom.get_program('5.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
