from typing import List
import Node
from Point import Point


class LineSegment(Node):
    """
    class to represent a line segment
    name: name of the line
    point1 : the starting point of the line. will be sorted so that it is always the first point from y-axis
    point2 : the end point of the line. it is the further point from the y-axis
    slope : slope of the line
    y_intercept : y_intercept of the line
    curr_y : value of the y coordinate for the current value of x in the sweep line status
    """
    __slots__ = "name", "point1", "point2", "slope", "y_intercept", "curr_y", "prev_y"

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
        self.prev_y = None

        self.name = name

        # y = mx + b
        # point1.y = m * point1.x + b
        # point2.y = m * point2.x + b
        # m = (point2.y - point1.y) / (point2.x - point1.x)
        # b = point1.y - {(point2.y - point1.y)/(point2.x - point1.x)} * point1.x
        self.y_intercept = point1.y - \
            ((point2.y - point1.y) / (point2.x - point1.x)) * point1.x

    def get_points(self) -> List[Point]:
        """
        gives the value of points making up the line segment
        :return: list of points
        """
        return [self.point1, self.point2]

    def set_curr_y(self, x):
        """
        sets the value of current y in the line segment
        :param x:
        :return: None
        """
        self.prev_y = self.curr_y
        self.curr_y = self.slope * x + self.y_intercept

    def get_curr_y(self, x):
        """
        gives the value of current y stored in the self
        :param x:
        :return: self.curr_y
        """
        return self.curr_y

    def get_other_point(self, point: Point):
        """
        gets the other point that make up the line segment
        :param point:
        :return: other point
        """
        if point == self.point1:
            return self.point2
        else:
            return self.point1

    def __str__(self):
        return self.name
