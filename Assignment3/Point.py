from enum import Enum

import Node


class PointType(Enum):
    """
    defines the types of the events that can occur
    """
    START_POINT = 0
    END_POINT = 1


class Point(Node.Node):
    """
    defines the point class
    stores the point x and y coordinates and the line segment it belongs to
    """
    __slots__ = "x", "y", "LineSegment", "point_type", "name", "trapezoid"

    def __init__(self, x: float, y: float, name="") -> None:
        super().__init__(Node.NodeType.X_NODE)
        self.x = x
        self.y = y
        # self.point_type = point_type
        self.LineSegment = None
        self.name = name
        self.trapezoid = None

    def set_segment(self, line):
        self.LineSegment = line

    def __str__(self):
        return "{" + str(self.x) + ", " + str(self.y) + "}"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Point):
            return False
        return round(self.x, 5) == round(o.x) and round(self.y, 5) == round(o.y, 5)
