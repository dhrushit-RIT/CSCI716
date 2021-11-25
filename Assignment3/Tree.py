
from typing import Union
from BoundingBox import BoundingBox

from LineSegment import LineSegment
from Node import Node, NodeType
from Point import Point
from Trapezoid import Trapezoid
from utils import Side

class Tree:
    root: Union[Node, None]

    def __init__(self, bounding_box: BoundingBox) -> None:
        self.root = bounding_box

    def addSegment(segment: LineSegment):
        pass

    def find_boudning_trapezoid(self, point: Point) -> Trapezoid:
        traverser = self.root
        if self.root is not None:
            while not isinstance(traverser, Trapezoid):
                if traverser.node_type == NodeType.X_NODE:
                    if point.x > traverser.x:
                        traverser = traverser.right
                    elif point.x == traverser.x:
                        if point.name.find("q") >= 0:
                            traverser = traverser.left
                        else:
                            traverser = traverser.right
                    else:
                        traverser = traverser.left
                    
                else:
                    # y - ax - b
                    value_for_point = traverser.get_value_for_point(point)
                    if value_for_point < 0:
                        traverser = traverser.right
                    elif value_for_point == 0:
                        if point == traverser.point1:
                            other_point_value = traverser.point2.y - point.y
                        else:
                            other_point_value = traverser.point1.y - point.y
                        
                        if other_point_value > 0:
                            traverser = traverser.right
                        else:
                            traverser = traverser.left

                    else:
                        traverser = traverser.left
        return traverser

    def replace_trapezoid_with(self, find_node: Trapezoid, replace_with: Node):

        if find_node == self.root:
            self.root = replace_with
        else:
            if len(find_node.parents) == 0:
                print(find_node.name, "parents unknown")
            for parent, side in find_node.parents:
                if side == Side.LEFT:
                    parent.left = replace_with
                elif side == Side.RIGHT:
                    parent.right = replace_with
                else:
                    print("ERROR replacing trapezoid node. can not determine Side")
        return find_node

    def find_boudning_trapezoid_path(self, point: Point) -> Trapezoid:
        traverser = self.root
        trav_path = []
        if self.root is not None:
            while not isinstance(traverser, Trapezoid):
                trav_path.append(traverser.name)
                if traverser.node_type == NodeType.X_NODE:
                    if point.x > traverser.x:
                        traverser = traverser.right
                    elif point.x == traverser.x:
                        if point.name.find("q") >= 0:
                            traverser = traverser.left
                        else:
                            traverser = traverser.right
                    else:
                        traverser = traverser.left
                    
                else:
                    # y - ax - b
                    value_for_point = traverser.get_value_for_point(point)
                    if value_for_point < 0:
                        traverser = traverser.right
                    elif value_for_point == 0:
                        if point == traverser.point1:
                            other_point_value = traverser.point2.y - point.y
                        else:
                            other_point_value = traverser.point1.y - point.y
                        
                        if other_point_value > 0:
                            traverser = traverser.right
                        else:
                            traverser = traverser.left

                    else:
                        traverser = traverser.left
        trav_path.append(traverser.name)
        return trav_path

    def __str__(self) -> str:
        return str(self.root) + "||"+str(self.root.left) + "||" + str(self.root.right)
