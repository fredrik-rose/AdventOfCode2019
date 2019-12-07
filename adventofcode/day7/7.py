# Day 7: Amplification Circuit
import itertools
import os
import sys

sys.path.append(os.path.join(sys.path[0], '..', 'intcodecomputer'))
import intcodecomputer as intcom


def part_one(program):
    max_output = -1000000  # inf.
    for phases in itertools.permutations(range(0, 5)):
        amp_input = 0
        for phase in phases:
            amp = intcom.run_program(program.copy())
            next(amp)
            amp.send(phase)
            amp_input = amp.send(amp_input)
        max_output = max(max_output, amp_input)
    print("Max amplifier output: {}".format(max_output))


def part_two(program):
    max_output = -1000000  # -inf.
    for phases in itertools.permutations(range(5, 10)):
        amp_input = 0
        amplifiers = [intcom.run_program(program.copy()) for _ in range(5)]
        for amp, phase in zip(amplifiers, phases):
            next(amp)
            amp.send(phase)
            amp_input = amp.send(amp_input)
        while True:
            try:
                for amp in amplifiers:
                    next(amp)
                    amp_input = amp.send(amp_input)
            except StopIteration:
                break
        max_output = max(max_output, amp_input)
    print("Max amplifier output: {}".format(max_output))


def main():
    program = intcom.get_program('7.txt')
    part_one(program.copy())
    part_two(program.copy())


if __name__ == "__main__":
    main()
