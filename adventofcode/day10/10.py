# Day 10: Monitoring Station
import collections as coll
import math

import numpy as np


ASTEROID = '#'


def get_asteroid_coordinates_from_map(asteroid_map):
    return [(x, y) for y, line in enumerate(asteroid_map) for x, char in enumerate(line) if char == ASTEROID]


def get_angles_to_asteriods(monitoring_station, asteroid_coordinates):
    relative_positions = (np.subtract(asteroid, monitoring_station)
                          for asteroid in asteroid_coordinates if asteroid != monitoring_station)
    return (tuple(pos // math.gcd(*pos)) for pos in relative_positions)


def get_best_monitoring_station(asteroid_coordinates):
    candidates = ((monitoring_station, len(set(get_angles_to_asteriods(monitoring_station, asteroid_coordinates))))
                  for monitoring_station in asteroid_coordinates)
    return max(candidates, key=lambda x: x[1])


def vaporize_asteriods(monitoring_station, asteroid_coordinates):
    angles = get_angles_to_asteriods(monitoring_station, asteroid_coordinates)
    asteroids = [(position, angle) for position, angle in zip(asteroid_coordinates, angles)]
    asteroids.sort(key=lambda x: (-math.atan2(x[1][0], x[1][1]), np.linalg.norm(x[1])))
    ranks = {asteroid: (coll.Counter(a[1] for a in asteroids[:i])[asteroid[1]], i)
             for i, asteroid in enumerate(asteroids)}
    asteroids.sort(key=lambda x: ranks[x])
    return [asteroid[0] for asteroid in asteroids]  # Asteroids in vaporization order.


def part_one(asteroid_map):
    asteroid_coordinates = get_asteroid_coordinates_from_map(asteroid_map)
    best_monitoring_station, max_number_of_visible_asteroids = get_best_monitoring_station(asteroid_coordinates)
    print("Number of asteroids detected from the best monitoring station asteroid: {} at {}"
          .format(max_number_of_visible_asteroids, best_monitoring_station))


def part_two(asteroid_map):
    asteroid_coordinates = get_asteroid_coordinates_from_map(asteroid_map)
    monitoring_station, _ = get_best_monitoring_station(asteroid_coordinates)
    asteroids_in_vaporization_order = vaporize_asteriods(monitoring_station, asteroid_coordinates)
    print("The 200:th asteroid to get vaporized is located at position: {}"
          .format(asteroids_in_vaporization_order[199]))


def main():
    with open('10.txt') as file:
        asteroid_map = [[char for char in line.strip()] for line in file]
    part_one(asteroid_map.copy())
    part_two(asteroid_map.copy())


if __name__ == "__main__":
    main()
