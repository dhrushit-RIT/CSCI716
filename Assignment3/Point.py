from enum import Enum

import Node


class PointType(Enum):
    """
    defines the types of the events that can occur
    """
    START_POINT = 0
    END_POINT = 1


class Point(Node):
    """
    defines the point class
    stores the point x and y coordinates and the line segment it belongs to
    """
    __slots__ = "x", "y", "line_segment", "point_type"

    def __init__(self, x: float, y: float, point_type: PointType) -> None:
        self.x = x
        self.y = y
        self.point_type = point_type
        self.line_segment = None

    def set_segment(self, line):
        self.line_segment = line

    def __str__(self):
        return "{" + str(self.x) + ", " + str(self.y) + "}"
