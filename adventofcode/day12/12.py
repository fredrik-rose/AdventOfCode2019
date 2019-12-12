# Day 12: The N-Body Problem
import functools
import math
import re

import numpy as np


def extract_ints(line):
    return [int(x) for x in re.findall(r'-?\d+', line)]


class Moon:
    def __init__(self, position):
        self.position = np.array(position)
        self.velocity = np.zeros(len(position), dtype=int)

    def __repr__(self):
        return 'pos={}, vel={}'.format(self.position, self.velocity)

    def move(self):
        self.position += self.velocity

    def potential_energy(self):
        return int(np.linalg.norm(self.position, ord=1))

    def kinetic_energy(self):
        return int(np.linalg.norm(self.velocity, ord=1))


def simulate(moons, time):
    for _ in range(time):
        apply_gravity(moons)
        move(moons)


def apply_gravity(moons):
    for affected_moon in moons:
        affected_moon.velocity += sum(np.sign(moon.position - affected_moon.position) for moon in moons)


def move(moons):
    for moon in moons:
        moon.move()


def get_energy(moons):
    return sum(moon.potential_energy() * moon.kinetic_energy() for moon in moons)


def part_one():
    with open('12.txt') as file:
        moons = [Moon(extract_ints(line)) for line in file]
    iterations = 1000
    simulate(moons, iterations)
    energy = get_energy(moons)
    print("Energy after {} iterations: {}".format(iterations, energy))


def simulate_1d(moons):
    def get_state():
        return tuple(e for m in moons for e in m)

    initial_state = get_state()
    iterations = 0
    while True:
        apply_gravity_1d(moons)
        move_1d(moons)
        iterations += 1
        if get_state() == initial_state:
            return iterations


def apply_gravity_1d(moons):
    for affected_moon in moons:
        affected_moon[1] += sum(np.sign(moon[0] - affected_moon[0]) for moon in moons)


def move_1d(moons):
    for moon in moons:
        moon[0] += moon[1]


def lcm(a, b):
    return int(a * b / math.gcd(a, b))


def part_two():
    with open('12.txt') as file:
        moons = [Moon(extract_ints(line)) for line in file]
    moons_1d = [[[moon.position[i], moon.velocity[i]] for moon in moons] for i in range(3)]
    periods_1d = [simulate_1d(moons) for moons in moons_1d]
    period_3d = functools.reduce(lcm, periods_1d)
    print("Number of steps to first repeating state: {}".format(period_3d))


def main():
    part_one()
    part_two()


if __name__ == "__main__":
    main()
