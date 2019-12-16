# Day 16: Flawed Frequency Transmission
import math

import numpy as np


def parse_signal(path):
    with open(path, 'r') as file:
        digits = [int(d) for d in file.read().strip('\n')]
        return digits


def run_fft(signal, phases):
    output_signal = np.array(signal)
    init_kernel = [0, 1, 0, -1]
    for _ in range(phases):
        kernel_matrix = []
        for i in range(len(output_signal)):
            kernel = [e for e in init_kernel for _ in range(i + 1)]
            if len(kernel) < len(output_signal) + 1:
                kernel *= int(math.ceil(len(output_signal) / len(kernel))) + 1
            kernel = kernel[1:len(output_signal) + 1]
            kernel_matrix.append(kernel)
        output_signal = np.dot(output_signal, np.array(kernel_matrix).T)
        output_signal = np.mod(np.abs(output_signal), 10)
    return output_signal


def part_one(signal):
    output_signal = run_fft(signal, 100)
    print("First eight digits in output signal: {}".format(''.join(str(d) for d in output_signal)[:8]))


def part_two(signal):
    signal = signal * 10000
    offset = int(''.join(str(d) for d in signal[:7]))
    # This is an exploit that only works if the offset points to the second part
    # of the input. The second part of the output is only depended on itself and
    # each element is easily calculated using an accumulated sum.
    assert(offset > len(signal) / 2)
    for _ in range(100):
        for i in range(-2, -len(signal) // 2, -1):
            signal[i] = (signal[i] + signal[i + 1]) % 10
    print("Message: {}".format(''.join(str(d) for d in signal[offset:offset + 8])))


def main():
    signal = parse_signal('16.txt')
    part_one(signal.copy())
    part_two(signal.copy())


if __name__ == "__main__":
    main()
