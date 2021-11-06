from typing import List
from LineSegment import LineSegment
from Point import Point, PointType


class BoundingBox:
    segements: List[LineSegment]
    lowerX: int
    lowerY: int
    upperX: int
    upperY: int

    botLine: LineSegment
    topLine: LineSegment
    leftLine: LineSegment
    rightLine: LineSegment

    def __init__(self, lowerX, lowerY, upperX, upperY) -> None:
        self.lowerX = lowerX
        self.lowerY = lowerY
        self.upperX = upperX
        self.upperY = upperY

        lowerLeft = Point(lowerX, lowerY, PointType.START_POINT)
        lowerRight = Point(upperX, lowerY, PointType.START_POINT)
        upperLeft = Point(lowerX, upperY, PointType.START_POINT)
        upperRight = Point(upperX, upperY, PointType.START_POINT)

        self.botLine = LineSegment(lowerLeft, lowerRight, "bot")
        self.topLine = LineSegment(upperLeft, upperRight, "top")
        self.rightLine = LineSegment(lowerRight, upperRight, "right")
        self.leftLine = LineSegment(lowerLeft, upperLeft, "left")

    def get_lines(self):
        return [self.botLine, self.topLine, self.rightLine, self.leftLine]
