import time
import sys

from util import Point, print_points
from util import plot_points_and_hull
from util import read_from_file
from util import write_to_file


def get_lowest_point(points) -> Point:
    """
    scans the list of points and returns the point with lowest y value
    :param points: the points to be considered
    :return: the point with the lowest y value
    """
    min_y_point = points[0]

    for point in points:
        if point.y < min_y_point.y:
            min_y_point = point
    return min_y_point


def orientation(p, q, r):
    """
    gives the orientation of the points going from p to q to r, as determined with right hand thumb rule
    :param p: first point
    :param q: second point
    :param r: third point
    :return: orientation of p-q-r
    """
    return q.x * r.y - r.x * q.y - p.x * r.y + p.x * q.y + r.x * p.y - q.x * p.y


def find_upper_hull(points):
    """
    calculates the points that make the upper hull in the list of points
    :param points: list of all the points to consider
    :return: list of points that make the upper hull
    """
    upper_points = []
    start_point = points[0]
    end_point = points[-1]
    min_y = min(start_point.y, end_point.y)

    # points below the min y of the two extremes do not matter
    # therefore filter them out
    for point in points:
        if point.y >= min_y:
            upper_points.append(point)
    upper_hull = []
    for i in range(3):
        if len(upper_points) > 0:
            upper_hull.append(upper_points.pop(0))

    if len(upper_hull) == 3:
        for point in upper_points:
            while len(upper_hull) >= 3 and orientation(upper_hull[-3], upper_hull[-2], upper_hull[-1]) >= 0:
                upper_hull.pop(-2)
            upper_hull.append(point)
        while len(upper_hull) >= 3 and orientation(upper_hull[-3], upper_hull[-2], upper_hull[-1]) >= 0:
            upper_hull.pop(-2)

    return upper_hull


def find_lower_hull(points):
    """
    calculates the points that make the lower hull in the list of points
    :param points: list of all the points to consider
    :return: list of points that make the upper hull
    """
    lower_points = []
    start_point = points[0]
    end_point = points[-1]
    min_y = max(start_point.y, end_point.y)

    # points above the max y of the two extremes do not matter
    # therefore filter them out
    for point in points:
        if point.y <= min_y:
            lower_points.append(point)

    lower_hull = []
    for i in range(3):
        if len(lower_points) > 0:
            lower_hull.append(lower_points.pop(0))

    if len(lower_hull) == 3:
        for point in lower_points:
            while len(lower_hull) >= 3 and orientation(lower_hull[-3], lower_hull[-2], lower_hull[-1]) <= 0:
                lower_hull.pop(-2)
            lower_hull.append(point)
        while len(lower_hull) >= 3 and orientation(lower_hull[-3], lower_hull[-2], lower_hull[-1]) <= 0:
            lower_hull.pop(-2)

    return lower_hull


def merge_hulls(lower_hull, upper_hull):
    """
    merges the lower hull with the upper hull and gives the list of resultant hull points
    :param lower_hull: points that make the lower hull
    :param upper_hull: points that make the upper hull
    :return: the points that make the combined hull
    """
    final_hull = lower_hull
    for point in reversed(upper_hull[1:-1]):
        final_hull.append(point)
    return final_hull


def graham_scan(points):
    """
    applies the graham scan algorithm to find the hull of the list of points
    :param points: points for which we need to find the convex hull
    :return: the list of points that makes up the convex hull
    """
    points = sorted(points, key=lambda point: point.x)

    upper_hull = find_upper_hull(points)
    lower_hull = find_lower_hull(points)
    final_hull = merge_hulls(lower_hull, upper_hull)
    print_points(final_hull)
    return final_hull


def main():
    """
    the driver function. it uses the file name for the list of points from the terminal.
    if not provided then it uses the points.txt as the default file
    :return:
    """
    filename = "points.txt"  # default file to use

    # use this file if the file name is provided
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    points = read_from_file(filename)

    # run and time the graham scan algorithm
    start_time = time.time()
    hull_graham_scan = graham_scan(points)
    end_time = time.time()
    hull_find_time = end_time - start_time

    # write the hull points to the file answer.txt
    write_to_file("answer.txt", hull_graham_scan)

    print("hull find time:", hull_find_time)

    # plot the final hull and the points
    plot_points_and_hull(points, hull_graham_scan)


if __name__ == "__main__":
    main()
