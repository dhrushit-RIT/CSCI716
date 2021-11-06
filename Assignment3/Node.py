
from typing import Union

from LineSegment import LineSegment
from Point import Point
from Trapazoid import Trapazoid


class Node:
    left: Union[LineSegment, Point, Trapazoid, None]
    right: Union[LineSegment, Point, Trapazoid, None]
