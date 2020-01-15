# Day 18: Many-Worlds Interpretation
import numpy as np
from scipy import ndimage as spimage


WALL = '#'
FREESPACE = '.'
INTERSECTION = '+'
START = '@'


class Node:
    def __init__(self, position, symbol):
        self.position = position
        self.symbol = symbol
        self.connections = []

    def __repr__(self):
        return "<{}, {}>".format(self.symbol if self.symbol != INTERSECTION else self.position,
                                 [n.symbol for n in self.connections])


def connect_nodes(a, b):
    a.connections.append(b)
    b.connections.append(a)


def distance_between_nodes(a, b):
    return np.sum(np.abs(np.array(a.position) - np.array(b.position)))


def convert_maze_to_graph(file_path):
    with open(file_path) as file:
        raw_data = [list(line) for line in file.read().splitlines()]
        char_array = np.array(raw_data)
    graph = create_graph(char_array)
    for l in char_array:
        print(''.join(l))
    # print(graph)
    return graph


def create_graph(char_array):
    cooridors = find_corridors(char_array)
    nodes = []
    nodes_above = [None] * char_array.shape[1]
    for y, line in enumerate(char_array):
        left_node = None
        assert line[0] == WALL
        assert line[-1] == WALL
        for x, char in enumerate(line):
            if char == WALL:
                nodes_above[x] = None
                left_node = None
                continue
            if char == FREESPACE and cooridors[y, x]:
                continue
            symbol = char_array[y, x]
            symbol = INTERSECTION if symbol == FREESPACE else symbol
            char_array[y, x] = symbol  # NOTE: Only for debug visualization.
            node = Node((y, x), symbol)
            if left_node:
                connect_nodes(node, left_node)
            if nodes_above[x]:
                connect_nodes(node, nodes_above[x])
            left_node = node
            nodes_above[x] = node
            if symbol == START:
                nodes.insert(0, node)
            else:
                nodes.append(node)
    return nodes


def find_corridors(char_array):
    char_array = char_array == WALL
    horizontal = np.array([[0, 0, 0],
                           [1, 0, 1],
                           [0, 0, 0]])
    vertical = np.array([[0, 1, 0],
                         [0, 0, 0],
                         [0, 1, 0]])
    horizontal_wall = spimage.minimum_filter(char_array, footprint=horizontal) == 1
    vertical_wall = spimage.minimum_filter(char_array, footprint=vertical) == 1
    horizontal_path = spimage.maximum_filter(char_array, footprint=horizontal) == 0
    vertical_path = spimage.maximum_filter(char_array, footprint=vertical) == 0
    corridors = np.logical_or(np.logical_and(horizontal_wall, vertical_path),
                              np.logical_and(vertical_wall, horizontal_path))
    return corridors


def breadth_first_search_3d(start, number_of_keys):
    visited = set()
    queue = [(start, frozenset(), 0)]
    while len(queue) > 0:
        node, keys, distance = queue.pop(0)
        if len(keys) == number_of_keys:
            return distance
        if (node, keys) in visited:
            continue
        visited.add((node, keys))
        for next_node in node.connections:
            if next_node.symbol.isupper() and next_node.symbol.lower() not in keys:
                # Door that we do not have the key to open.
                continue
            next_keys = set(keys)
            if next_node.symbol.islower():
                # Key.
                next_keys.add(next_node.symbol)
            queue.append((next_node, frozenset(next_keys), distance + distance_between_nodes(node, next_node)))
    else:
        print("ERROR: Could not find all keys.")


def part_one():
    graph = convert_maze_to_graph('18.txt')
    number_of_keys = len([k for k in graph if k.symbol.islower()])
    shortest_path_length = breadth_first_search_3d(graph[0], number_of_keys)
    print("The length of the shortest path to collect all keys for part one is: {}".format(shortest_path_length))


def part_two():
    # Assumes that each quadrant can be solved independently with doors in other quadrants already opened.
    # Offer a goat before proceeding to hopefully receive enough luck for the assumption above to hold.
    shortest_path_length = 0
    for file_path in ('18_tl.txt', '18_tr.txt', '18_bl.txt', '18_br.txt'):
        graph = convert_maze_to_graph(file_path)
        keys = [k for k in graph if k.symbol.islower()]
        doors = (d for d in graph if d.symbol.isupper())
        for d in doors:
            # Open doors that does not have a corresponding key.
            if d.symbol.lower() not in keys:
                d.symbol = INTERSECTION
        number_of_keys = len(keys)
        shortest_path_length += breadth_first_search_3d(graph[0], number_of_keys)
    print("The length of the shortest path to collect all keys for part two is: {}".format(shortest_path_length))


def main():
    part_one()
    part_two()


if __name__ == "__main__":
    main()
