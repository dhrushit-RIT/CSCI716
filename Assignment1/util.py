import matplotlib.pyplot as plt
import math


class Point:
    """
    Class of points
    """
    __slots__ = "x", "y"

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y


class LineSegment:
    """
    Class of line segments
    """
    __slots__ = "point1", "point2", "slope", "length"

    def has_point(self, point):
        """
        check if one of the points is point
        :param point: the point to compare other points with
        :return: True if the point is same as one of the points of line segment
        """
        return self.point1 == point or self.point2 == point

    def swap_points(self):
        """
        Swaps the order of points of the current line segment
        :return: None
        """
        self.point1, self.point2 = self.point2, self.point1

    def __init__(self, point1, point2) -> None:
        """
        Initialise the line
        :param point1: point 1 of the line
        :param point2: point 2 of the line
        """
        self.point1 = point1
        self.point2 = point2
        if point2.x != point1.x:
            self.slope = (point2.y - point1.y) / (point2.x - point1.x)
        else:
            self.slope = None
        self.length = math.sqrt(
            (point2.y - point1.y) * (point2.y - point1.y) + (point2.x - point1.x) * (point2.x - point1.x))

    def __eq__(self, o: object) -> bool:
        """
        Define how to compare the lines
        :param o: other line
        :return: True if the other line is same as this line other wise False
        """
        return (self.point1 == o.point1 and self.point2 == o.point2) or (
                self.point1 == o.point2 and self.point2 == o.point1)

    def __str__(self) -> str:
        """
        String representation of the line
        :return:
        """
        return "<" + str(self.point1) + "-" + str(self.point2) + ">"


def sign(num):
    """
    gives the sign of the number
    :param num: the number whose sign is needed
    :return: +1 if the number is positive or 0 else -1
    """
    if num == 0:
        return 0
    elif num < 0:
        return -1
    else:
        return 1


def print_points(points):
    """
    Print the linst of points one at a time
    :param points:
    :return:
    """
    for point in points:
        print(point, end=" ")
    print()


def print_lines(lines, tag):
    """
    Prints the list of lines one at a time
    :param lines: list of lines to print
    :param tag: descriptor that print along with the lines
    :return:
    """
    if tag:
        print(tag)
    for line in lines:
        print(line)
    print()


def plot_points_and_hull(points, hull):
    """
    plots the list of points and hull using the matplotlib library
    :param points: list of points to be plotted
    :param hull: list of points making the hull
    :return: None
    """
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
    """
    writes the list of points -- points to the file mentioned
    :param filename: name of the file to write to
    :param points: list of points to write to the file
    :return: None
    """
    print("writing to file")
    with open(filename, 'w') as f:
        f.write(str(len(points)) + "\n")
        for point in points:
            f.write(str(point) + "\n")


def read_from_file(filename):
    """
    reads the file and makes a list of points
    :param filename: name of the file
    :return: list of points read from the file in a list data structure
    """
    with open(filename) as f:
        num_points = f.readline()
        points = []
        for line in f:
            line = line.strip()
            x, y = line.split()
            points.append(Point(float(x), float(y)))
    return points


def get_lowest_point(points) -> Point:
    """
    Calculates the lowest in the list of points by value in y coordinate
    :param points: list of points to check
    :return: point that has the lowest y value
    """
    min_y_point = points[0]

    for point in points:
        if point.y < min_y_point.y:
            min_y_point = point
    return min_y_point
