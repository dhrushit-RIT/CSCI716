"""
plane_sweep_line_segment_intersection.py

implements the place sweep algorithm for line intersection

This algorithm finds the intersection points of line segments that are non-vertical

It is assumed that the lines are not vertical
It is assumed that more than two lines do not intersect at the same point

Author: Dhrushit Raval <dr9703@rit.edu>
"""

from enum import Enum
from typing import Tuple, List, Set
from pytreemap import TreeSet
import sys
import matplotlib.pyplot as plt


# set this to false if you want to show the plot
SAVE_TO_FILE = True


class EventType(Enum):
    """
    defines the types of the events that can occur
    """
    START_POINT = 0
    END_POINT = 1
    INTERSECTION = 2


class Point:
    """
    defines the point class
    stores the point x and y coordinates and the line segment it belongs to
    """
    __slots__ = "x", "y", "line_segment", "point_type"

    def __init__(self, x: float, y: float, point_type: EventType) -> None:
        self.x = x
        self.y = y
        self.point_type = point_type
        self.line_segment = None

    def set_segment(self, line):
        self.line_segment = line

    def __str__(self):
        return "{" + str(self.x) + ", " + str(self.y) + "}"


class LineSegment:
    """
    class to represent a line segment
    name: name of the line
    point1 : the starting point of the line. will be sorted so that it is always the first point from y-axis
    point2 : the end point of the line. it is the further point from the y-axis
    slope : slope of the line
    y_intercept : y_intercept of the line
    curr_y : value of the y coordinate for the current value of x in the sweep line status
    """
    __slots__ = "name", "point1", "point2", "slope", "y_intercept", "curr_y"

    def __init__(self, point1, point2, name="") -> None:
        self.point1 = point1
        self.point2 = point2

        if self.point1.x > self.point2.x:
            self.point1, self.point2 = self.point2, self.point1

        if self.point1.x - self.point2.x != 0:
            self.slope = (self.point2.y - self.point1.y) / \
                         (self.point2.x - self.point1.x)
        else:
            self.slope = None

        self.curr_y = None

        self.name = name

        # y = mx + b
        # point1.y = m * point1.x + b
        # point2.y = m * point2.x + b
        # m = (point2.y - point1.y) / (point2.x - point1.x)
        # b = point1.y - {(point2.y - point1.y)/(point2.x - point1.x)} * point1.x
        self.y_intercept = point1.y - \
                           ((point2.y - point1.y) / (point2.x - point1.x)) * point1.x

    def get_points(self) -> List[Point]:
        return [self.point1, self.point2]

    def set_curr_y(self, x):
        self.curr_y = self.slope * x + self.y_intercept

    def get_curr_y(self, x):
        self.curr_y = self.slope * x + self.y_intercept
        return self.curr_y

    def get_other_point(self, point: Point):
        if point == self.point1:
            return self.point2
        else:
            return self.point1

    def __str__(self):
        return self.name


class Event:
    """
    defines the events class
    point : the point associated with this event
    event_type : the type of event (EventType)
    lines : set if the point is an intersection point
    """
    __slots__ = "point", "event_type", "lines"

    def __init__(self, point: Point, event_type: EventType) -> None:
        self.point = point
        self.event_type = event_type
        self.lines = None

    def set_event_lines(self, lines: List[LineSegment]):
        if self.event_type == EventType.INTERSECTION:
            if not self.lines:
                self.lines = lines
            else:
                self.lines.extend(lines)
            self.lines.sort(key=lambda x: x.curr_y)

    def __str__(self):
        return str(self.point) + " " + str(self.event_type) + " " + self.lines


class SweepLineStatus:
    """
    sweep line status class
    ordered_BST: the ordered BST that holds the line segments in order
    x : the current value of x when processing a given event
    """
    __slots__ = "ordered_BST", "x"

    def __str__(self):
        return str(x) + " " + str(self.ordered_BST)

    def __init__(self, comp) -> None:
        self.ordered_BST = TreeSet(comp)
        self.x = -9999999999

    def set_status(self, x):
        self.x = x

    def get_sequenced_line_segments(self, l1: LineSegment, l2: LineSegment):
        if self.ordered_BST.contains(l1) and self.ordered_BST.contains(l2):
            if self.ordered_BST.lower(l1) == l2:
                return [l2, l1]
            else:
                return [l1, l2]


def cmp_event(e1: Event, e2: Event):
    """
    comparison function to compare two events

    :param e1: first event
    :param e2: second evednt
    :return: integer 1 if e1 happens after e2, -1 if e1 happens before e2 and 0 if both event are equally likely to occur now
    """
    if e1.point.x < e2.point.x:
        return -1
    elif e1.point.x > e2.point.x:
        return 1
    else:
        if e1.event_type == EventType.INTERSECTION and e2.event_type != EventType.INTERSECTION:
            return -1
        elif e2.event_type == EventType.INTERSECTION and e1.event_type != EventType.INTERSECTION:
            return 1
        else:
            if e1.event_type == EventType.START_POINT and e2.event_type == EventType.END_POINT:
                return -1
            elif e1.event_type == EventType.END_POINT and e2.event_type == EventType.START_POINT:
                return 1
            else:
                # issue here
                # TODO fix this
                if e1.point.line_segment != e2.point.line_segment:
                    if e1.point.line_segment.get_other_point(e1.point).x < e2.point.line_segment.get_other_point(
                            e2.point).x:
                        return -1
                    else:
                        return 1
                else:
                    return 0
                # return 0


def cmp_line(l1: LineSegment, l2: LineSegment):
    """
    function to compare two line segments
    :param l1: first line segment
    :param l2: second line segment
    :return: 1 if l1's current y coordinate value > l2's. -1 other wise and 0 if both y values are same
    """
    y_1 = round(l1.curr_y, 5)
    y_2 = round(l2.curr_y, 5)
    if y_1 < y_2:
        return -1
    elif y_1 > y_2:
        return 1
    else:
        if l1 == l2:
            return 0
        else:
            return 1


def read_file() -> List[LineSegment]:
    """
    reads the file and creates structured array and line segments
    :return:
    """
    filename = sys.argv[1]
    data_points = []

    line_counter = 0

    with open(filename) as f:
        f.readline()

        for line in f:
            points = [float(x) for x in line.strip().split()]
            p1 = Point(points[0], points[1], EventType.START_POINT)
            p2 = Point(points[2], points[3], EventType.END_POINT)
            line_segment = LineSegment(p1, p2, "line" + str(line_counter))
            p1.set_segment(line_segment)
            p2.set_segment(line_segment)
            line_counter += 1

            data_points.append(line_segment)
    return data_points


def check_if_intersecting_in_range(l1: LineSegment, l2: LineSegment):

    """
    checks if the line segments intersect within a given set of conditions

    :param l1: line 1 line segment
    :param l2: line 2 line segment
    :return: tuple of whether there was an intersection and if so, what point
    """
    x1 = l1.point1.x
    y1 = l1.point1.y
    x2 = l1.point2.x
    y2 = l1.point2.y

    x3 = l2.point1.x
    y3 = l2.point1.y
    x4 = l2.point2.x
    y4 = l2.point2.y

    t1_numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t1_denominator = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))

    t2_numerator = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)
    t2_denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # does not handle the vertical lines
    # assuming no lines are vertical or horizontal
    t1_in_range = t1_denominator != 0 and 0 <= t1_numerator / t1_denominator <= 1
    t2_in_range = t2_denominator != 0 and 0 <= t2_numerator / t2_denominator <= 1

    intersection_point = None
    if t1_in_range and t2_in_range:
        t1 = t1_numerator / t1_denominator
        t2 = t2_numerator / t2_denominator

        intersection_point = Point(x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1), EventType.INTERSECTION)

    return t1_in_range and t2_in_range, intersection_point


def check_for_intersection(event_queue: TreeSet, l1: LineSegment, l2: LineSegment, sweep_line_status: SweepLineStatus):
    """
    checks for the intersection of the line segments and adds to the event queue

    :param event_queue: the queue of events to add a new event to
    :param l1: first of the two intersecting lines
    :param l2: second of the two intersecting lines
    :param sweep_line_status: data structure for maintaining the line segments in sorted order of y at a given x
    :return: None
    """
    intersecting_in_range, intersection_point = check_if_intersecting_in_range(
        l1, l2)

    if intersecting_in_range:
        if intersection_point.x > sweep_line_status.x:
            intersection_event = Event(
                intersection_point, EventType.INTERSECTION)

            # check for the sequence of lines and then add
            lines_sorted_by_y = sorted([l1, l2],
                                       key=lambda x: -x.get_curr_y(sweep_line_status.x))
            intersection_event.set_event_lines(lines_sorted_by_y)
            if not event_queue.contains(intersection_event):
                event_queue.add(intersection_event)


def handle_event(event: Event, event_queue: TreeSet, sweep_line_status: SweepLineStatus,
                 line_intersections: Set[Point]):
    """
    handles the current event
    event could be one of the three event types

    :param event: the event that occurred
    :param event_queue: queue to add the event to
    :param sweep_line_status: data structure for maintaining the line segments in sorted order of y at a given x
    :param line_intersections: list of line intersections
    :return: None
    """
    if event.event_type == EventType.START_POINT:
        # add to sweep line status
        sweep_line_status.ordered_BST.add(event.point.line_segment)
        # check if it intersects with successor
        successor_line = sweep_line_status.ordered_BST.higher(
            event.point.line_segment)
        if successor_line:
            check_for_intersection(
                event_queue, event.point.line_segment, successor_line, sweep_line_status)
        # check if it intersects with predecessor
        predecessor_line = sweep_line_status.ordered_BST.lower(
            event.point.line_segment)
        if predecessor_line:
            check_for_intersection(
                event_queue, event.point.line_segment, predecessor_line, sweep_line_status)

    elif event.event_type == EventType.END_POINT:
        line_to_remove = event.point.line_segment

        # find the line segments prior and after the line to remove
        predecessor_line = sweep_line_status.ordered_BST.lower(line_to_remove)
        successor_line = sweep_line_status.ordered_BST.higher(line_to_remove)

        # remove the line from the sweep line status
        sweep_line_status.ordered_BST.remove(line_to_remove)
        # check for the intersection of the lines that are now adjecent
        if predecessor_line and successor_line:
            check_for_intersection(
                event_queue, predecessor_line, successor_line, sweep_line_status)
    else:
        l0 = event.lines[0]
        l1 = event.lines[1]
        sweep_line_status.ordered_BST.remove(l0)
        sweep_line_status.ordered_BST.remove(l1)
        sweep_line_status.ordered_BST.add(l1)
        sweep_line_status.ordered_BST.add(l0)

        # remove all the events from the queue
        # add all of them with the reversed order for the intersection point lines
        # check if after reversal, there is an intersection
        new_predecessor_of_l1 = sweep_line_status.ordered_BST.lower(l1)
        if new_predecessor_of_l1:
            check_for_intersection(event_queue, l1, new_predecessor_of_l1, sweep_line_status)
        new_successor_of_l0 = sweep_line_status.ordered_BST.higher(l0)
        if new_successor_of_l0:
            check_for_intersection(event_queue, l0, new_successor_of_l0, sweep_line_status)

        line_intersections.add(event.point)


def cmp_points_tuples(t1: Tuple[Point, LineSegment, LineSegment], t2: Tuple[Point, LineSegment, LineSegment]):
    """
    comparison function to compare two points from a tuple containing the point and line segments intersecting at that point
    :param t1: first tuples
    :param t2: second typle
    :return: 0 if points are the same. 1 if the first tuple is greater than the second -1 if otherwise
    """
    if round(t1[0].x, 5) == round(t2[0].x, 5) and round(t1[0].y, 5) == round(t2[0].y, 5):
        return 0
    else:
        return 1 if t1[0].x > t2[0].x else -1


def cmp_points(p1: Point, p2: Point):
    """
    compares two points
    :param p1: first point
    :param p2: second point
    :return: 0 if two points are same upto 5 places after decimal
    """
    if round(p1.x, 5) == round(p2.x, 5) and round(p1.y, 5) == round(p2.y, 5):
        return 0
    else:
        return 1 if p1.x > p2.x else -1


def update_all_lines(line_segments: List[LineSegment], sweep_line_status: SweepLineStatus):
    """
    sets the current y value for the line segments based on the current x vlaue in the sweep line status
    :param line_segments: list of line segments to update
    :param sweep_line_status: sweep line status
    :return: None
    """
    for line_segment in line_segments:
        if line_segment.point1.x <= sweep_line_status.x <= line_segment.point2.x:
            line_segment.set_curr_y(sweep_line_status.x)


def find_intersections(line_segments: List[LineSegment]):
    """
    find the intersections between all the line segments using the plane sweep algorithm
    :param line_segments: list of line segments to find the intersections for
    :return: list of intersections between these lines
    """
    line_intersections = TreeSet(cmp_points)
    event_queue = TreeSet(cmp_event)
    sweep_line_status = SweepLineStatus(cmp_line)

    for line_segment in line_segments:
        points = line_segment.get_points()

        event_queue.add(Event(points[0], EventType.START_POINT))
        event_queue.add(Event(points[1], EventType.END_POINT))

    while not event_queue.is_empty():
        event: Event = event_queue.poll_first()
        sweep_line_status.set_status(event.point.x)
        update_all_lines(line_segments, sweep_line_status)
        handle_event(event, event_queue, sweep_line_status, line_intersections)
        for point in line_intersections:
            print(point, end=" ")
        print()
    return line_intersections


def find_intersections_brute_force(line_segments):
    """
    finds the intersections between every line using the brute force approach
    :param line_segments: list of line segments to find the intersections for
    :return: list of line intersections
    """
    intersections = []
    for l1 in line_segments:
        for l2 in line_segments:
            if l1 != l2:
                intersecting_in_range, intersection_point = check_if_intersecting_in_range(
                    l1, l2)
                if intersecting_in_range:
                    intersections.append((intersection_point, l1.name, l2.name))
    line_intersections = TreeSet(cmp_points_tuples)

    for intersection in intersections:
        line_intersections.add(intersection)
    for point in line_intersections:
        print(point[0], point[1], point[2])


def plot_lines_and_intersections(line_segments: List[LineSegment], intersections: List[Point]):
    """
    plots the list of line segments and the line intersection points on the graph
    stores it if SAVE_TO_FILE is true
    else shows the plot in a new window
    :param line_segments: list of line segments to plot
    :param intersections: intersection points found in the list of line segments
    :return: None
    """
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    x = []
    y = []
    for line in line_segments:
        points = line.get_points()
        ax.plot([points[0].x, points[1].x], [points[0].y, points[1].y])  # Plot some data on the axes.

    for intersection in intersections:
        ax.scatter(intersection.x, intersection.y)
    if SAVE_TO_FILE:
        plt.savefig("output.png")
    else:
        plt.show()


def main():
    """
    driver function
    :return: None
    """
    line_segments = read_file()
    intersections = find_intersections(line_segments)
    # find_intersections_brute_force(line_segments)

    plot_lines_and_intersections(line_segments, intersections)


if __name__ == "__main__":
    main()
