import sys
import time

from util import LineSegment, print_points
from util import plot_points_and_hull
from util import read_from_file


def sign(num):
    if num == 0:
        return 0
    elif num < 0:
        return -1
    else:
        return 1


def all_points_on_one_side(point1, point2, points):
    # Line : y = mx + b
    # y - mx - b = 0 for all points on this line
    # y - mx - b < 0 for points on left
    # y - mx - b > 0 for points on right
    if point2.x != point1.x:
        slope = (point2.y - point1.y) / (point2.x - point1.x)
    else:
        slope = None
    if slope is not None:
        y_intercept = point1.y - slope * point1.x
    else:
        y_intercept = None

    side = 0

    for point in points:  # O(n)
        if point != point1 and point != point2:
            if slope is not None:
                point_side = sign(point.y - slope * point.x -
                                  y_intercept)  # O(1)
            else:
                if point.x > point1.x:
                    point_side = 1
                elif point.x == point1.x:
                    point_side = 0
                else:
                    point_side = -1
            if side == 0:
                side = point_side
            else:
                if point_side != 0 and point_side != side:
                    return False
                else:
                    continue
    return True


def brute_force(points):
    print("finding answer to life universe and everything")
    hull_lines = []
    for point1 in points:
        for point2 in points:
            if point1 != point2:
                # print("point1", point1, "point2", point2)
                if all_points_on_one_side(point1, point2, points):
                    line_segment = LineSegment(point1, point2)
                    if line_segment not in hull_lines:
                        hull_lines.append(line_segment)
                else:
                    # print("all points on either side")
                    continue

    return hull_lines


def order_lines(lines):
    print("ordering lines:")
    sequenced_lines = [lines[0]]
    first_line = lines[0]
    lines.pop(0)
    while True:
        last_line = sequenced_lines[-1]
        if len(sequenced_lines) > 1 and last_line.has_point(first_line.point1):
            break
        else:
            next_line = None
            for line in lines:
                if line.has_point(last_line.point2) and line != last_line:
                    if line.point1 != last_line.point2:
                        line.swap_points()
                    sequenced_lines.append(line)
                    lines.remove(line)
                    break
            # if sequenced_lines[-1] in lines:
            #     lines.remove(sequenced_lines[-1])
    return sequenced_lines


def get_points_from_lines(lines):
    """
        pre: the lines are ordered in a sequence and lines has at least 3 points
    """
    print("fetching points from the lines")
    points = []
    if lines[1].point1 == lines[0].point1 or lines[1].point2 == lines[0].point1:
        points.append(lines[0].point2)
        points.append(lines[0].point1)
    else:
        points.append(lines[0].point1)
        points.append(lines[0].point2)

    for line in lines[1:-1]:
        if line.point1 == points[-1]:
            points.append(line.point2)
        else:
            points.append(line.point1)
    return points


def delete_collinear_lines(lines):
    print("deleting collinear lines")
    lines_to_remove = []
    for line1 in lines:
        for line2 in lines:
            if line1 != line2:
                if line1.slope == line2.slope:
                    if line2.has_point(line1.point1) or line2.has_point(line1.point2):
                        if line1.length < line2.length:
                            if line1 not in lines_to_remove:
                                lines_to_remove.append(line1)

    for line in lines_to_remove:
        lines.remove(line)

    return lines


def write_to_file(filename, points):
    print("writing to file")
    with open(filename, 'w') as f:
        f.write(str(len(points)) + "\n")
        for point in points:
            f.write(str(point) + "\n")


def orientation(p, q, r):
    return q.x * r.y - r.x * q.y - p.x * r.y + p.x * q.y + r.x * p.y - q.x * p.y


def make_counter_clockwise(points):
    if orientation(points[0], points[1], points[2]) < 0:
        points.reverse()
    return points


def main():
    filename = "points.txt"
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    points = read_from_file(filename)
    start_time = time.time()
    hull_brute_force = brute_force(points)  # all points on one side of the line
    end_time = time.time()
    hull_find_time = end_time - start_time

    start_time = time.time()
    non_collinear_lines = delete_collinear_lines(hull_brute_force)
    ordered_lines = order_lines(non_collinear_lines)
    hull_points = get_points_from_lines(ordered_lines)

    ccw_points = make_counter_clockwise(hull_points)
    end_time = time.time()
    post_process_time = end_time - start_time
    print_points(ccw_points)
    write_to_file("answer.txt", ccw_points)

    print("time to find hull:", hull_find_time)
    print("time to post process(sequence, order etc):", post_process_time)

    plot_points_and_hull(points, ccw_points)


if __name__ == "__main__":
    main()
