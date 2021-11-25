
from enum import Enum
from typing import Union


class NodeType(Enum):
    X_NODE = 0
    Y_NODE = 1
    LEAF = 2


class Node:
    left: Union['Node', None]
    right: Union['Node', None]
    node_type: NodeType

    def __init__(self, node_type) -> None:
        self.left = None
        self.right = None
        self.node_type = node_type

    def __str__(self) -> str:
        s = str(self)
        if self.left:
            s += str(self.left)
        if self.right:
            s += str(self.right)
        return s
