import matplotlib.pyplot as plt
import math


class Point:
    __slots__ = "x", "y"

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y


class LineSegment:
    __slots__ = "point1", "point2", "slope", "length"

    def has_point(self, point):
        return self.point1 == point or self.point2 == point

    def swap_points(self):
        self.point1, self.point2 = self.point2, self.point1

    def __init__(self, point1, point2) -> None:
        self.point1 = point1
        self.point2 = point2
        if point2.x != point1.x:
            self.slope = (point2.y - point1.y) / (point2.x - point1.x)
        else:
            self.slope = None
        self.length = math.sqrt(
            (point2.y - point1.y) * (point2.y - point1.y) + (point2.x - point1.x) * (point2.x - point1.x))

    def __eq__(self, o: object) -> bool:
        return (self.point1 == o.point1 and self.point2 == o.point2) or (
                self.point1 == o.point2 and self.point2 == o.point1)

    def __str__(self) -> str:
        return "<" + str(self.point1) + "-" + str(self.point2) + ">"


def print_points(points):
    for point in points:
        print(point, end=" ")
    print()


def print_lines(lines, tag):
    if tag:
        print(tag)
    for line in lines:
        print(line)
    print()


def plot_points_and_hull(points, hull):
    fig = plt.figure()
    x_arr = [p.x for p in points]
    y_arr = [p.y for p in points]
    plt.plot(x_arr, y_arr, 'ro')
    hull.append(hull[0])
    hull_x_arr = [h.x for h in hull]
    hull_y_arr = [h.y for h in hull]
    plt.plot(hull_x_arr, hull_y_arr)
    plt.show()


def write_to_file(filename, points):
    print("writing to file")
    with open(filename, 'w') as f:
        f.write(str(len(points)) + "\n")
        for point in points:
            f.write(str(point) + "\n")


def read_from_file(filename):
    with open(filename) as f:
        num_points = f.readline()
        points = []
        for line in f:
            line = line.strip()
            x, y = line.split()
            points.append(Point(float(x), float(y)))
    return points


def get_lowest_point(points) -> Point:
    min_y_point = points[0]

    for point in points:
        if point.y < min_y_point.y:
            min_y_point = point
    return min_y_point
