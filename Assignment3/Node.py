
from enum import Enum
from typing import Union

from LineSegment import LineSegment
from Point import Point
from Trapazoid import Trapazoid


class NodeType(Enum):
    X_NODE = 0
    Y_NODE = 1


class Node:
    left: Union['Node', None]
    right: Union['Node', None]
    node_type: NodeType
