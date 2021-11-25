from typing import List
from LineSegment import LineSegment
from Node import Node
from Point import Point, PointType
from Trapezoid import Trapezoid
from Wall import Wall


class BoundingBox(Trapezoid):
    segements: List[LineSegment]
    lowerX: int
    lowerY: int
    upperX: int
    upperY: int

    bot_line: LineSegment
    top_line: LineSegment
    left_line: Wall
    right_line: Wall

    def __init__(self, lowerX, lowerY, upperX, upperY) -> None:
        self.lowerX = lowerX
        self.lowerY = lowerY
        self.upperX = upperX
        self.upperY = upperY

        lowerLeft = Point(lowerX, lowerY)
        lowerRight = Point(upperX, lowerY)
        upperLeft = Point(lowerX, upperY)
        upperRight = Point(upperX, upperY)

        self.bot_line = LineSegment(lowerLeft, lowerRight, "bot")
        self.top_line = LineSegment(upperLeft, upperRight, "top")
        self.right_line = Wall(lowerRight, upperRight, "right")
        self.left_line = Wall(lowerLeft, upperLeft, "left")

    def get_lines(self):
        return [self.bot_line, self.top_line, self.right_line, self.left_line]

    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)
