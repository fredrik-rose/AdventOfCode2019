# Day 20: Donut Maze
import collections as coll

import numpy as np


EMPTY = ' '
WALL = '#'
FREESPACE = '.'
NODE = 'o'
PORTAL = '@'
START = 'AA'
END = 'ZZ'


class Node:
    def __init__(self, position, symbol):
        self.position = position
        self.symbol = symbol
        self.connections = []
        self.level = 0

    def __repr__(self):
        return "<{}, {}, {}>".format(self.symbol, self.position, [n.symbol for n in self.connections])

    def connect(self, node):
        self.connections.append(node)
        node.connections.append(self)


def parse_input_to_graph(file_path):
    char_array = read_maze_from_file(file_path)
    portals = find_portals(char_array)
    graph = create_graph(char_array)
    start, end = add_portals_to_graph(portals, graph)
    # NOTE: Debug visualization.
    print("Graph with portals (represented by '{}'):".format(PORTAL))
    for l in char_array:
        print(''.join(l))
    return start, end


def read_maze_from_file(file_path):
    with open(file_path) as file:
        raw_data = [list(line) for line in file.read().splitlines()]
        char_array = np.array(raw_data)
    return char_array


def find_portals(char_array):
    portals = coll.defaultdict(list)
    for y, line in enumerate(char_array):
        for x, char in enumerate(line):
            if char == FREESPACE:
                candidate_portals = (char_array[y - 2:y, x],
                                     char_array[y + 1:y + 3, x],
                                     char_array[y, x - 2:x],
                                     char_array[y, x + 1:x + 3])
                for candidate in candidate_portals:
                    if np.all(np.char.isupper(candidate)):
                        portals[''.join(candidate)].append((y, x))
                        char_array[(y, x)] = PORTAL  # NOTE: Only for debug visualization.
    return portals


def create_graph(char_array):
    nodes = []
    nodes_above = [None] * char_array.shape[1]
    for y, line in enumerate(char_array):
        left_node = None
        for x, char in enumerate(line):
            if char == WALL or char.isupper():
                nodes_above[x] = None
                left_node = None
                continue
            if char == EMPTY:
                continue
            if char_array[y, x] == FREESPACE:
                char_array[y, x] = NODE  # NOTE: Only for debug visualization.
            node = Node((y, x), NODE)
            if left_node:
                node.connect(left_node)
            if nodes_above[x]:
                node.connect(nodes_above[x])
            left_node = node
            nodes_above[x] = node
            nodes.append(node)
    return nodes


def add_portals_to_graph(portals, graph):
    def set_level(node):
        min_y = min(n.position[0] for n in graph)
        max_y = max(n.position[0] for n in graph)
        min_x = min(n.position[1] for n in graph)
        max_x = max(n.position[1] for n in graph)
        if node.position[0] == min_y or node.position[0] == max_y:
            node.level = -1
        elif node.position[1] == min_x or node.position[1] == max_x:
            node.level = -1
        else:
            node.level = 1

    start_position = portals.pop(START)[0]
    end_position = portals.pop(END)[0]
    graph_lookup = {n.position: n for n in graph}
    start_node = graph_lookup[start_position]
    end_node = graph_lookup[end_position]
    start_node.symbol = START
    end_node.symbol = END
    for name, portal_pair in portals.items():
        portal_a = graph_lookup[portal_pair[0]]
        portal_b = graph_lookup[portal_pair[1]]
        for portal in (portal_a, portal_b):
            portal.symbol = name
            set_level(portal)
        portal_a.connect(portal_b)
    return start_node, end_node


def breadth_first_search(start, end):
    visited = set()
    queue = [(start, 0)]
    while len(queue) > 0:
        node, distance = queue.pop(0)
        if node == end:
            return distance
        if node in visited:
            continue
        visited.add(node)
        for next_node in node.connections:
            queue.append((next_node, distance + 1))
    else:
        print("ERROR: Could not find path.")


def breadth_first_search_3d(start, end):
    visited = set()
    queue = [(start, 0, 0)]
    while len(queue) > 0:
        node, level, distance = queue.pop(0)
        if node == end and level == 0:
            return distance
        if (node, level) in visited:
            continue
        visited.add((node, level))
        for next_node in node.connections:
            next_level = level
            if node.symbol == next_node.symbol and node.symbol.isupper():
                # Walk trough portal.
                next_level += node.level
            if next_level < 0:
                continue
            if next_node.symbol in (START, END) and level > 0:
                # Only active at level 0.
                continue
            queue.append((next_node, next_level, distance + 1))
    else:
        print("ERROR: Could not find all keys.")


def part_one(start, end):
    distance = breadth_first_search(start, end)
    print("Part one distance: {}".format(distance))


def part_two(start, end):
    distance = breadth_first_search_3d(start, end)
    print("Part two distance: {}".format(distance))


def main():
    start, end = parse_input_to_graph('20.txt')
    part_one(start, end)
    part_two(start, end)


if __name__ == "__main__":
    main()
