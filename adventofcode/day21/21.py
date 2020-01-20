# Day 21: Springdroid Adventure
import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


def part_one(program):
    springscript = (
        # Always jump to the first after a hole. If the closest contains a hole
        # jump and hope for the best.
        'NOT C T\n',
        'AND D T\n',
        'NOT A J\n',
        'OR T J\n',
        'WALK\n',
    )
    output = intcom.run_ascii(program, springscript)
    print("Hull damage (part one): {}".format(output))


def part_two(program):
    springscript = (
        # Check if any of the three closest are holes. (1)
        # Check if we can do two consecutive jumps. (2)
        # Check if the closest contains a hole. (3)
        # If (1 and 2) or 3 do a jump.
        'NOT A T\n',
        'NOT B J\n',
        'OR J T\n',
        'NOT C J\n',
        'OR T J\n',
        'AND D J\n',
        'AND H J\n',
        'NOT A T\n',
        'OR T J\n',
        'RUN\n',
    )
    output = intcom.run_ascii(program, springscript)
    print("Hull damage (part two): {}".format(output))


def main():
    program = intcom.get_program('21.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
