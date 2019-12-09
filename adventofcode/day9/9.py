# Day 9: Sensor Boost
import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


def part_one(program):
    computer = intcom.run_program(program)
    next(computer)
    print(computer.send(1))
    for output in computer:
        print(output)


def part_two(program):
    computer = intcom.run_program(program)
    next(computer)
    print(computer.send(2))


def main():
    program = intcom.get_program('9.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
