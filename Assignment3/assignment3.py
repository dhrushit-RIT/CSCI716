from typing import List, Union
from BoundingBox import BoundingBox

from LineSegment import LineSegment
from Point import Point
from Trapazoid import Trapazoid


def read_input():

    line_segments = {}
    with open("intput.txt") as f:
        f.readline()
        bounding_box_points = f.readline().strip().split()

        bounding_box = BoundingBox(
            bounding_box_points[0],
            bounding_box_points[1],
            bounding_box_points[2],
            bounding_box_points[3]
        )

        bounding_lines = bounding_box.get_lines()
        # for line in bounding_lines:
        #     line_segments[line.name] = line

        line_counter = 1
        while line in f:
            line = line.strip()
            x1, y1, x2, y2 = line.split()
            if x1 <= x2:
                p1 = Point(x1, y1)
                p2 = Point(x2, y2)
            else:
                p1 = Point(x2, y2)
                p2 = Point(x1, y1)

            line_name = "l"+str(line_counter)
            line_counter += 1
            l = LineSegment(p1, p2)
            line_segments[line_name] = l

    return line_segments, bounding_box


def main():
    line_segments, bounding_box = read_input()
    

if __name__ == "__main__":
    main()
