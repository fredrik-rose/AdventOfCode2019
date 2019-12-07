# Day 3: Crossed Wires
from matplotlib import pyplot as plt


def line_interection(x1, y1, x2, y2, x3, y3, x4, y4):
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


def convert_wire_to_points(wire):
    def decode_action(action):
        direction = action[0]
        length = int(action[1:])
        if direction == 'R':
            return (length, 0)
        elif direction == 'L':
            return (-length, 0)
        elif direction == 'U':
            return (0, length)
        elif direction == 'D':
            return (0, -length)
        else:
            print("ERROR: Invalid action!")

    position = [0, 0]
    points = [position.copy()]
    for edge in wire:
        movement = decode_action(edge)
        position[0] += movement[0]
        position[1] += movement[1]
        points.append(position.copy())
    return points


def polyline_manhattan_intersections(points_a, points_b):
    min_distance = 1000000  # inf.
    for (x1, y1), (x2, y2) in zip(points_a[:-1], points_a[1:]):
        for (x3, y3), (x4, y4) in zip(points_b[:-1], points_b[1:]):
            intersection = line_interection(x1, y1, x2, y2, x3, y3, x4, y4)
            if intersection:
                manhattan_distance = abs(intersection[0]) + abs(intersection[1])
                if manhattan_distance > 0:
                    min_distance = min(min_distance, manhattan_distance)
    return min_distance


def polyline_path_intersections(points_a, points_b):
    def distance_between_points(x1, y1, x2, y2):
        return (abs(x1 - x2), abs(y1 - y2))

    min_distance = 1000000  # inf.
    distance_a = [0, 0]
    for (x1, y1), (x2, y2) in zip(points_a[:-1], points_a[1:]):
        distance_b = [0, 0]
        for (x3, y3), (x4, y4) in zip(points_b[:-1], points_b[1:]):
            intersection = line_interection(x1, y1, x2, y2, x3, y3, x4, y4)
            if intersection:
                manhattan_distance = abs(intersection[0]) + abs(intersection[1])
                if manhattan_distance > 0:
                    point_diff_a = distance_between_points(x1, y1, intersection[0], intersection[1])
                    point_diff_b = distance_between_points(x3, y3, intersection[0], intersection[1])
                    intersection_distance_a = distance_a[0] + distance_a[1] + point_diff_a[0] + point_diff_a[1]
                    intersection_distance_b = distance_b[0] + distance_b[1] + point_diff_b[0] + point_diff_b[1]
                    distance = intersection_distance_a + intersection_distance_b
                    min_distance = min(min_distance, distance)
            distance_diff_b = distance_between_points(x3, y3, x4, y4)
            distance_b[0] += distance_diff_b[0]
            distance_b[1] += distance_diff_b[1]
        distance_diff_a = distance_between_points(x1, y1, x2, y2)
        distance_a[0] += distance_diff_a[0]
        distance_a[1] += distance_diff_a[1]
    return min_distance


def plot_plylines(polyline_a, polyline_b):
    points_a_x = [e[0] for e in polyline_a]
    points_a_y = [e[1] for e in polyline_a]
    points_b_x = [e[0] for e in polyline_b]
    points_b_y = [e[1] for e in polyline_b]
    plt.plot(points_a_x, points_a_y, '+-')
    plt.plot(points_b_x, points_b_y, '+-')
    plt.show()


def part_one(polyline_a, polyline_b):
    distance = polyline_manhattan_intersections(polyline_a, polyline_b)
    print("Manhattan distance: {}".format(int(distance)))


def part_two(polyline_a, polyline_b):
    distance = polyline_path_intersections(polyline_a, polyline_b)
    print("Min distance: {}".format(int(distance)))


def main():
    with open('3.txt') as f:
        wire_a = [e for e in f.readline().split(',')]
        wire_b = [e for e in f.readline().split(',')]
    # wire_a = ["R8", "U5", "L5", "D3"]
    # wire_b = ["U7", "R6", "D4", "L4"]
    # wire_a = ["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"]
    # wire_b = ["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"]
    # wire_a = ["R98", "U47", "R26", "D63", "R33", "U87", "L62", "D20", "R33", "U53", "R51"]
    # wire_b = ["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"]
    polyline_a = convert_wire_to_points(wire_a)
    polyline_b = convert_wire_to_points(wire_b)
    plot_plylines(polyline_a, polyline_b)
    part_one(polyline_a.copy(), polyline_b.copy())
    part_two(polyline_a.copy(), polyline_b.copy())


if __name__ == "__main__":
    main()
