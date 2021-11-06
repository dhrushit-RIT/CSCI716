
from typing import Union

from LineSegment import LineSegment
from Point import Point
from Trapazoid import Trapazoid


class Tree:
    root: Union[LineSegment, Point, Trapazoid, None]
    pass
