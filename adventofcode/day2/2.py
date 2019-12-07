# Day 2: 1202 Program Alarm
import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


def part_one(program):
    program[1] = 12
    program[2] = 2
    for _ in intcom.run_program(program):
        pass
    print(program[0])


def part_two(init_program):
    for i in range(0, 100):
        for j in range(0, 100):
            program = init_program.copy()
            program[1] = i
            program[2] = j
            for _ in intcom.run_program(program):
                pass
            if program[0] == 19690720:
                print("noun: {}, verb: {}, 100 * noun + verb: {}".format(i, j, 100 * i + j))


def main():
    program = intcom.get_program('2.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
