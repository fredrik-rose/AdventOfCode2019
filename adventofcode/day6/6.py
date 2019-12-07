# Day 6: Universal Orbit Map
import collections as coll


CENTER_OF_MASS = 'COM'


def get_input(path):
    with open(path) as file:
        return file.read().splitlines()


def create_space(space_map):
    space = coll.defaultdict(list)
    for orbit in space_map:
        planet, satellite = orbit.split(')')  # Format: planet)satellite
        space[planet].append(satellite)
    return space


def count_orbits(space, planet, count=0):
    return count + sum(count_orbits(space, p, count + 1) for p in space[planet])


def path_to_planet(space, planet_to_find):
    def path_finder(planet, path):
        if planet == planet_to_find:
            return True
        for p in space[planet]:
            path.append(p)
            if path_finder(p, path):
                return True
            path.pop()
        return False

    result_path = []
    if not path_finder(CENTER_OF_MASS, result_path):
        print("ERROR: Could not find path to {}".format(planet_to_find))
    return result_path


def shortest_path(space, planet_a, planet_b):
    path_a = set(path_to_planet(space, planet_a)[:-1])
    path_b = set(path_to_planet(space, planet_b)[:-1])
    return len(path_a ^ path_b)


def part_one():
    space_map = ['COM)B',
                 'B)C',
                 'C)D',
                 'D)E',
                 'E)F',
                 'B)G',
                 'G)H',
                 'D)I',
                 'E)J',
                 'J)K',
                 'K)L']
    space_map = get_input('6.txt')
    space = create_space(space_map)
    orbits = count_orbits(space, CENTER_OF_MASS)
    print("Number of direct and indirect orbits: {}".format(orbits))


def part_two():
    space_map = ['COM)B',
                 'B)C',
                 'C)D',
                 'D)E',
                 'E)F',
                 'B)G',
                 'G)H',
                 'D)I',
                 'E)J',
                 'J)K',
                 'K)L',
                 'K)YOU',
                 'I)SAN']
    space_map = get_input('6.txt')
    space = create_space(space_map)
    length_of_shortest_path = shortest_path(space, 'YOU', 'SAN')
    print("Length of shortest path between '{}' and '{}': {}".format('YOU', 'SAN', length_of_shortest_path))


def main():
    part_one()
    part_two()


if __name__ == "__main__":
    main()
