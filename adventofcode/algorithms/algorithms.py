# Some generic good-to-have stuff.
import math
import re


def pass_data_to_a_generator():
    # Example of how data can be passed to a generator.
    def generator():
        a = yield
        print(a)

    gen = generator()
    next(gen)
    try:
        gen.send("Hello World!")
    except StopIteration:
        pass


def extract_ints(line):
    # Extracts all ints on a line of text.
    return [int(x) for x in re.findall(r'-?\d+', line)]


def lcm(a, b):
    # Least-common multiplier.
    return int(a * b / math.gcd(a, b))


def exp_by_squaring(x, n):
    # Calculates x raised to the power of n by squaring.
    assert n >= 0
    if n == 0:
        return 1
    elif n == 1:
        return x
    elif is_even(n):
        return exp_by_squaring(x * x, n // 2)
    elif is_odd(n):
        return x * exp_by_squaring(x * x, (n - 1) // 2)


def is_even(x):
    return (x % 2) == 0


def is_odd(x):
    return not is_even(x)


def modular_inverse(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # Calculates the intersection (if any) of two lines defined by to pairs of points each.
    den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if den != 0.0:
        t_num = (x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)
        u_num = (x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3)
        t = t_num / den
        u = -u_num / den
        if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
            px = x1 + t*(x2 - x1)
            py = y1 + t*(y2 - y1)
            return (px, py)
    return None


graph = {'A': [('B', 10), ('C', 5)],
         'B': [('A', 10), ('D', 9)],
         'C': [],
         'D': [],
         'E': []}

def dijkstra(graph, start, end):
    # Dijkstra's shortest-path algorithm.
    def get_distance_to_node(node):
        return distances[node][0]

    unvisited = set(graph.keys())
    distances = {node: (math.inf, None) for node in graph.keys()}  # {node: (total_distance_to_node, previous_node)}.
    distances[start] = (0, None)
    current_node = start
    # Find the shortest path from start to end.
    while current_node != end:
        distance_to_current = get_distance_to_node(current_node)
        if distance_to_current == math.inf:
            # Could not find path to end.
            break
        for node, distance in graph[current_node]:
            if node in unvisited:
                tentative_distance = distance_to_current + distance
                if tentative_distance < get_distance_to_node(node):
                    distances[node] = (tentative_distance, current_node)
        unvisited.remove(current_node)
        current_node = min(unvisited, key=get_distance_to_node)
    # Backtrack the shortest path.
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = distances[node][1]
    return distances[end][0], path[::-1]


graph = {'A': ['B', 'C'],
         'B': ['A', 'D'],
         'C': ['E'],
         'D': ['E'],
         'E': []}

def breadth_first_search(graph, start, end):
    # Finds shortest path (only the length, not the actual path) from start to end using breath-first search.
    visited = set()
    queue = [(start, 0)]
    while len(queue) > 0:
        node, distance = queue.pop(0)
        if node == end:
            return distance
        if node in visited:
            continue
        visited.add(node)
        for next_node in graph[node]:
            queue.append((next_node, distance + 1))
    else:
        print("ERROR: Could not find path.")
        return math.inf
