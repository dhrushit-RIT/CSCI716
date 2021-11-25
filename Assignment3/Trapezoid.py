from typing import List, Tuple
from LineSegment import LineSegment
from Node import Node
from Node import NodeType
from Wall import Wall
from utils import Side


class Trapezoid(Node):
    """
    Class defining Trapezoids
    """
    left_line: Wall
    right_line: Wall
    top_line: LineSegment
    bot_line: LineSegment
    name: str

    parents: List[Tuple[Node, Side]]

    def __init__(self, left_line, right_line, top_line, bot_line, name="") -> None:
        super().__init__(NodeType.LEAF)
        self.left_line = left_line
        self.right_line = right_line
        self.top_line = top_line
        self.bot_line = bot_line
        self.parents = []
        self.name = name

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Trapezoid):
            return False
        return self.left_line == o.left_line and self.right_line == o.right_line and self.top_line == o.top_line and self.bot_line == o.bot_line

    def merge_trapezoids(trap1: 'Trapezoid', trap2: 'Trapezoid', trap_num: int):
        if trap1.left_line == trap2.right_line:
            return Trapezoid(trap2.left_line, trap1.right_line,
                             LineSegment(trap2.top_line.point1, trap1.top_line.point2),
                             LineSegment(trap2.bot_line.point1, trap1.bot_line.point2), "T" + str(trap_num))
        elif trap1.right_line == trap2.left_line:
            return Trapezoid(trap1.left_line, trap2.right_line,
                             LineSegment(trap1.top_line.point1, trap2.top_line.point2),
                             LineSegment(trap1.bot_line.point1, trap2.bot_line.point2), "T" + str(trap_num))
        else:
            return None

    def add_parent(self, node, side):
        self.parents.append((node, side))

    def has_line(self, line: LineSegment):
        return line == self.top_line or line == self.bot_line or line == self.right_line or line == self.left_line

    def is_zero_area(self):
        if self.top_line.point1 == self.bot_line.point1 and self.top_line.point2 == self.bot_line.point2:
            return True
        return False

    def __str__(self) -> str:
        return self.name + " : " + str(self.top_line.point1) + ", " + str(self.top_line.point2) + " " + str(
            self.bot_line.point1) + " " + str(self.bot_line.point2)
