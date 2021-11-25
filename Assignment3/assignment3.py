
from typing import List, Union

from matplotlib import colors
from BoundingBox import BoundingBox

from LineSegment import LineSegment
from Point import Point
from Trapezoid import Trapezoid
from TrapezoidHolder import TrapezoidHolder
from Wall import Wall

import matplotlib.pyplot as plt


import random

import copy

from Tree import Tree

import matplotlib.pyplot as plt

from utils import Side

random.seed(259)

trap_counter = 1


def print_traps(th: TrapezoidHolder):
    print("-------------------------------------------------")
    for trap in th.lst:
        print(trap)
    print("=================================================")


def read_input():

    line_segments = {}
    with open("input.txt") as f:
        f.readline()
        bounding_box_points = [float(x) for x in f.readline().strip().split()]

        bounding_box = BoundingBox(
            bounding_box_points[0],
            bounding_box_points[1],
            bounding_box_points[2],
            bounding_box_points[3]
        )

        bounding_lines = bounding_box.get_lines()
        # for line in bounding_lines:
        #     line_segments[line.name] = line

        line_counter = 1
        point_counter = 1
        for line in f:
            line = line.strip()
            x1, y1, x2, y2 = [float(x) for x in line.split()]
            if x1 <= x2:
                p1 = Point(x1, y1, "p" + str(point_counter))
                p2 = Point(x2, y2, "q" + str(point_counter))
            else:
                p1 = Point(x2, y2, "p" + str(point_counter))
                p2 = Point(x1, y1, "q" + str(point_counter))

            line_name = "l"+str(line_counter)
            l = LineSegment(p1, p2, "L" + str(line_counter))
            line_counter += 1
            point_counter += 1
            line_segments[line_name] = l

    return line_segments, bounding_box


def get_left_trapezoid(bounding_trapezoid_start: Trapezoid, line_segment: LineSegment, wall_start: Wall, th: TrapezoidHolder, ph: List[Point]):
    global trap_counter
    top_left = bounding_trapezoid_start.top_line.point1
    top_right = Point(line_segment.point1.x, bounding_trapezoid_start.top_line.get_y_at(
        line_segment.point1.x))
    bot_left = bounding_trapezoid_start.bot_line.point1
    bot_right = Point(line_segment.point1.x, bounding_trapezoid_start.bot_line.get_y_at(
        line_segment.point1.x))

    left_line = Wall(top_left, bot_left,
                     bounding_trapezoid_start.left_line.starting_point)
    right_line = Wall(top_right, bot_right, line_segment.point1)
    top_line = LineSegment(top_left, top_right)
    bot_line = LineSegment(bot_left, bot_right)

    if line_segment.point1 in ph and line_segment.point1.trapezoid is not None:
        left_trapezoid = line_segment.point1.trapezoid
    else:
        left_trapezoid = Trapezoid(
            left_line,
            right_line,
            top_line,
            bot_line,
            "T" + str(trap_counter))
        trap_counter += 1

    #  andrew glassner ml and anim

    left_trapezoid = th.add_or_get_trapezoid(left_trapezoid)
    line_segment.point1.trapezoid = left_trapezoid

    return left_trapezoid


def get_top_trapezoid(bounding_box: BoundingBox, line_segment: LineSegment, th: TrapezoidHolder):

    top_left = Point(line_segment.point1.x,
                     bounding_box.top_line.get_y_at(line_segment.point1.x))
    top_right = Point(line_segment.point2.x,
                      bounding_box.top_line.get_y_at(line_segment.point2.x))
    bot_left = line_segment.point1
    bot_right = line_segment.point2

    left_line = Wall(top_left, bot_left, line_segment.point1)
    right_line = Wall(top_right, bot_right, line_segment.point2)
    top_line = LineSegment(top_left, top_right)
    bot_line = LineSegment(bot_left, bot_right)

    global trap_counter
    trapezoid = Trapezoid(
        left_line, right_line, top_line, bot_line, "T"+str(trap_counter))
    trap_counter += 1

    trapezoid = th.add_or_get_trapezoid(trapezoid)
    return trapezoid


def get_bot_trapezoid(bounding_box: BoundingBox, line_segment: LineSegment, th: TrapezoidHolder):

    top_left = line_segment.point1
    top_right = line_segment.point2
    bot_left = Point(line_segment.point1.x,
                     bounding_box.bot_line.get_y_at(line_segment.point1.x))
    bot_right = Point(line_segment.point2.x,
                      bounding_box.bot_line.get_y_at(line_segment.point2.x))

    left_line = Wall(top_left, bot_left, line_segment.point1)
    right_line = Wall(top_right, bot_right, line_segment.point2)
    top_line = LineSegment(top_left, top_right)
    bot_line = LineSegment(bot_left, bot_right)

    global trap_counter
    trapezoid = Trapezoid(
        left_line, right_line, top_line, bot_line, "T"+str(trap_counter))
    trap_counter += 1
    trapezoid = th.add_or_get_trapezoid(trapezoid)
    return trapezoid


def get_right_trapezoid(bounding_trapezoid_end: Trapezoid, line_segment: LineSegment, wall_end: Wall, th: TrapezoidHolder, ph: List[Point]):

    top_left = Point(line_segment.point2.x, bounding_trapezoid_end.top_line.get_y_at(
        line_segment.point2.x))
    top_right = bounding_trapezoid_end.top_line.point2
    bot_left = Point(line_segment.point2.x, bounding_trapezoid_end.bot_line.get_y_at(
        line_segment.point2.x))
    bot_right = bounding_trapezoid_end.bot_line.point2

    left_line_X = Wall(top_left, bot_left, line_segment.point2)
    right_line_X = Wall(top_right, bot_right,
                        bounding_trapezoid_end.right_line.starting_point)
    top_line_X = LineSegment(top_left, top_right)
    bot_line_X = LineSegment(bot_left, bot_right)

    global trap_counter

    point = [x for x in ph if x == line_segment.point2][0]

    if line_segment.point2 in ph and point.trapezoid is not None:
        right_trapezoid = point.trapezoid
    else:
        right_trapezoid = Trapezoid(
            left_line_X,
            right_line_X,
            top_line_X,
            bot_line_X,
            "T" + str(trap_counter))
        trap_counter += 1

    right_trapezoid = th.add_or_get_trapezoid(right_trapezoid)
    line_segment.point2.trapezoid = right_trapezoid

    return right_trapezoid


def case2(random_line: LineSegment, bounding_trapezoid_start: Trapezoid, bounding_trapezoid_end: Trapezoid, wall_start: Wall, wall_end: Wall, th: TrapezoidHolder, t: Tree, ph: List[Point]):
    left_trapezoid = get_left_trapezoid(
        bounding_trapezoid_start, random_line, wall_start, th, ph)
    top_trapezoid = get_top_trapezoid(
        bounding_trapezoid_start, random_line, th)
    bot_trapezoid = get_bot_trapezoid(
        bounding_trapezoid_start, random_line, th)
    right_trapezoid = get_right_trapezoid(
        bounding_trapezoid_end, random_line, wall_end, th, ph)

    replacement_node = random_line.point1
    replacement_node.left = left_trapezoid
    replacement_node.right = random_line.point2
    random_line.point2.left = random_line
    random_line.point2.right = right_trapezoid
    random_line.left = top_trapezoid
    random_line.right = bot_trapezoid

    left_trapezoid.add_parent(replacement_node, Side.LEFT)
    right_trapezoid.add_parent(random_line.point2, Side.RIGHT)
    top_trapezoid.add_parent(random_line, Side.LEFT)
    bot_trapezoid.add_parent(random_line, Side.RIGHT)

    if replacement_node is not None:
        t.replace_trapezoid_with(
            bounding_trapezoid_start, replacement_node)
        th.remove_trapezoid_from_lst(bounding_trapezoid_start)
    return replacement_node


def find_spanning_trapezoids(line_segment: LineSegment, th: TrapezoidHolder):
    spanning_trapezoids: List[Trapezoid] = []
    for trap in th.get_trapezoids():
        top_left = trap.top_line.point1
        top_right = trap.top_line.point2
        bot_left = trap.bot_line.point1
        bot_right = trap.bot_line.point2

        start_point_left_of_trap = line_segment.point1.x < top_left.x and line_segment.point1.x < top_right.x
        end_point_right_of_trap = line_segment.point2.x > top_left.x and line_segment.point2.x > top_right.x

        if start_point_left_of_trap and end_point_right_of_trap:
            left_y = line_segment.get_y_at(top_left.x)
            right_y = line_segment.get_y_at(top_right.x)
            if left_y < top_left.y and left_y > bot_left.y and right_y < top_right.y and right_y > bot_right.y:
                spanning_trapezoids.append(trap)

    return spanning_trapezoids


def find_spanning_trapezoids_case_3(line_segment: LineSegment, th: TrapezoidHolder):
    spanning_trapezoids: List[Trapezoid] = []
    for trap in th.get_trapezoids():
        top_left = trap.top_line.point1
        top_right = trap.top_line.point2
        bot_left = trap.bot_line.point1
        bot_right = trap.bot_line.point2

        start_point_left_of_trap = line_segment.point1.x <= top_left.x and line_segment.point1.x <= top_right.x
        end_point_right_of_trap = line_segment.point2.x >= top_left.x and line_segment.point2.x >= top_right.x

        # start_point_left_of_trap = line_segment.point1.x < top_left.x and line_segment.point1.x < top_right.x
        # end_point_right_of_trap = line_segment.point2.x > top_left.x and line_segment.point2.x > top_right.x

        if start_point_left_of_trap and end_point_right_of_trap:
            left_y = line_segment.get_y_at(top_left.x)
            right_y = line_segment.get_y_at(top_right.x)
            if left_y <= top_left.y and left_y >= bot_left.y and right_y <= top_right.y and right_y >= bot_right.y:
                spanning_trapezoids.append(trap)

    return spanning_trapezoids


def get_top_trapezoid_from_bounding_left(line_segment: LineSegment, bounding_trapezoid: Trapezoid, th: TrapezoidHolder):

    top_left = Point(line_segment.point1.x,
                     bounding_trapezoid.top_line.get_y_at(line_segment.point1.x))
    top_right = bounding_trapezoid.top_line.point2
    bot_left = line_segment.point1
    bot_right = Point(bounding_trapezoid.top_line.point2.x,
                      line_segment.get_y_at(bounding_trapezoid.top_line.point2.x))

    left_line = Wall(top_left, bot_left, bot_left)
    right_line = Wall(top_right, bot_right,
                      bounding_trapezoid.right_line.starting_point)
    top_line = LineSegment(top_left, top_right)
    bot_line = LineSegment(bot_left, bot_right)

    global trap_counter
    top_trapezoid = Trapezoid(
        left_line, right_line, top_line, bot_line, "T" + str(trap_counter))
    trap_counter += 1
    top_trapezoid = th.add_or_get_trapezoid(top_trapezoid)
    return top_trapezoid


def get_bot_trapezoid_from_bounding_left(line_segment: LineSegment, bounding_trapezoid: Trapezoid, th: TrapezoidHolder):

    top_left = line_segment.point1
    top_right = Point(bounding_trapezoid.top_line.point2.x,
                      line_segment.get_y_at(bounding_trapezoid.top_line.point2.x))
    bot_left = Point(line_segment.point1.x,
                     bounding_trapezoid.bot_line.get_y_at(line_segment.point1.x))
    bot_right = bounding_trapezoid.bot_line.point2

    left_line = Wall(top_left, bot_left, line_segment.point1)
    right_line = Wall(top_right, bot_right,
                      bounding_trapezoid.right_line.starting_point)
    top_line = LineSegment(top_left, top_right)
    bot_line = LineSegment(bot_left, bot_right)

    global trap_counter
    trapezoid = Trapezoid(
        left_line, right_line, top_line, bot_line, "T" + str(trap_counter))
    trap_counter += 1

    trapezoid = th.add_or_get_trapezoid(trapezoid)
    return trapezoid


def get_bot_trapezoid_from_bounding_right(line_segment: LineSegment, bounding_trapezoid: Trapezoid, th: TrapezoidHolder):

    top_left = Point(bounding_trapezoid.top_line.point1.x,
                     line_segment.get_y_at(bounding_trapezoid.top_line.point1.x))
    top_right = line_segment.point2
    bot_left = bounding_trapezoid.bot_line.point1
    bot_right = Point(line_segment.point2.x,
                      bounding_trapezoid.bot_line.get_y_at(line_segment.point2.x))

    left_line_Y = Wall(top_left, bot_left,
                       bounding_trapezoid.left_line.starting_point)
    right_line_Y = Wall(top_right, bot_right, line_segment.point2)
    top_line_Y = LineSegment(top_left, top_right)
    bot_line_Y = LineSegment(bot_left, bot_right)

    global trap_counter
    bot_trapezoid = Trapezoid(
        left_line_Y, right_line_Y, top_line_Y, bot_line_Y, "T" + str(trap_counter))
    trap_counter += 1

    bot_trapezoid = th.add_or_get_trapezoid(bot_trapezoid)
    return bot_trapezoid


def get_top_trapezoid_from_bounding_right(line_segment: LineSegment, bounding_trapezoid: Trapezoid, th: TrapezoidHolder):

    top_left = bounding_trapezoid.top_line.point1
    top_right = Point(line_segment.point2.x,
                      bounding_trapezoid.top_line.get_y_at(line_segment.point2.x))
    bot_left = Point(bounding_trapezoid.top_line.point1.x,
                     line_segment.get_y_at(bounding_trapezoid.top_line.point1.x))
    bot_right = line_segment.point2

    left_line_Y = Wall(top_left, bot_left,
                       bounding_trapezoid.left_line.starting_point)
    right_line_Y = Wall(top_right, bot_right, line_segment.point2)
    top_line_Y = LineSegment(top_left, top_right)
    bot_line_Y = LineSegment(bot_left, bot_right)

    global trap_counter
    top_trapezoid = Trapezoid(
        left_line_Y, right_line_Y, top_line_Y, bot_line_Y, "T"+str(trap_counter))
    trap_counter += 1

    top_trapezoid = th.add_or_get_trapezoid(top_trapezoid)
    return top_trapezoid


def case1(random_line: LineSegment, bounding_trapezoid_start: Trapezoid, bounding_trapezoid_end: Trapezoid, wall_start: Wall, wall_end: Wall, th: TrapezoidHolder, t: Tree, ph: List[Point]):

    # destroy and replace left end point
    # destroy and replace right end point
    # common trapezoid created with

    # for left point
    left_trapezoid = get_left_trapezoid(
        bounding_trapezoid_start, random_line, wall_start, th, ph)
    top_trapezoid_left = get_top_trapezoid_from_bounding_left(
        random_line, bounding_trapezoid_start, th)
    bot_trapezoid_left = get_bot_trapezoid_from_bounding_left(
        random_line, bounding_trapezoid_start, th)

    replacement_node = random_line.point1
    replacement_node.left = left_trapezoid
    replacement_node.right = random_line
    random_line.left = top_trapezoid_left
    random_line.right = bot_trapezoid_left

    left_trapezoid.add_parent(replacement_node, Side.LEFT)
    bot_trapezoid_left.add_parent(random_line, Side.RIGHT)
    top_trapezoid_left.add_parent(random_line, Side.LEFT)

    if replacement_node is not None:
        t.replace_trapezoid_with(
            bounding_trapezoid_start, replacement_node)
        th.remove_trapezoid_from_lst(bounding_trapezoid_start)
        # remove the parent references from the removed trapezoid later

    # for right point
    top_trapezoid_right = get_top_trapezoid_from_bounding_right(
        random_line, bounding_trapezoid_end, th)
    bot_trapezoid_right = get_bot_trapezoid_from_bounding_right(
        random_line, bounding_trapezoid_end, th)
    right_trapezoid = get_right_trapezoid(
        bounding_trapezoid_end, random_line, wall_end, th, ph)

    random_line_copy = copy.deepcopy(random_line)
    replacement_node = random_line_copy.point2
    replacement_node.left = random_line_copy
    replacement_node.right = right_trapezoid
    random_line_copy.left = top_trapezoid_right
    random_line_copy.right = bot_trapezoid_right

    right_trapezoid.add_parent(replacement_node, Side.RIGHT)
    top_trapezoid_right.add_parent(random_line_copy, Side.LEFT)
    bot_trapezoid_right.add_parent(random_line_copy, Side.RIGHT)

    if replacement_node is not None:
        t.replace_trapezoid_with(
            bounding_trapezoid_end, replacement_node)
        th.remove_trapezoid_from_lst(bounding_trapezoid_end)

    global trap_counter
    merged_trapezoids_top = Trapezoid.merge_trapezoids(
        top_trapezoid_left, top_trapezoid_right, trap_counter)
    if merged_trapezoids_top:
        th.add_or_get_trapezoid(merged_trapezoids_top)
        trap_counter += 1
    merged_trapezoids_bot = Trapezoid.merge_trapezoids(
        bot_trapezoid_left, bot_trapezoid_right, trap_counter)
    if merged_trapezoids_bot:
        trp = th.add_or_get_trapezoid(merged_trapezoids_bot)
        trap_counter += 1

    if merged_trapezoids_top is not None:
        th.remove_trapezoid_from_lst(top_trapezoid_left)
        th.remove_trapezoid_from_lst(top_trapezoid_right)
        random_line_copy.left = merged_trapezoids_top
        random_line.left = merged_trapezoids_top
        merged_trapezoids_top.parents.extend(top_trapezoid_left.parents)
        merged_trapezoids_top.parents.extend(top_trapezoid_right.parents)

    elif merged_trapezoids_bot is not None:
        merged_trapezoids_bot.parents.extend(bot_trapezoid_left.parents)
        merged_trapezoids_bot.parents.extend(bot_trapezoid_right.parents)
        th.remove_trapezoid_from_lst(bot_trapezoid_left)
        th.remove_trapezoid_from_lst(bot_trapezoid_right)
        random_line_copy.right = merged_trapezoids_bot
        random_line.right = merged_trapezoids_bot

    else:
        print("issue in case 2 with merging trapezoids")


def merge_trapezoids(traps: List[Trapezoid], th: TrapezoidHolder):
    global trap_counter

    while len(traps) > 1:
        merged_trap = Trapezoid.merge_trapezoids(
            traps[0], traps[1], trap_counter)
        if merged_trap is None:
            traps.pop(0)
        if merged_trap:
            merged_trap = th.add_or_get_trapezoid(merged_trap)
            trap_counter += 1

            if merged_trap in traps:
                if merged_trap == traps[0]:
                    merged_trap.parents.extend(traps[1].parents)
                    th.remove_trapezoid_from_lst(traps[1])
                    traps.pop(1)
                else:
                    merged_trap.parents.extend(traps[0].parents)
                    th.remove_trapezoid_from_lst(traps[0])
                    traps.pop(0)
                continue

            t1_parents = traps[0].parents
            t2_parents = traps[1].parents

            for parent, side in t1_parents:
                if side == Side.LEFT:
                    parent.left = merged_trap
                elif side == Side.RIGHT:
                    parent.right = merged_trap
                else:
                    print("ERROR adding merged trap to the parent")

                merged_trap.add_parent(parent, side)

            for parent, side in t2_parents:
                if side == Side.LEFT:
                    parent.left = merged_trap
                elif side == Side.RIGHT:
                    parent.right = merged_trap
                else:
                    print("ERROR adding merged trap to the parent")

                merged_trap.add_parent(parent, side)

            th.remove_trapezoid_from_lst(traps[0])
            th.remove_trapezoid_from_lst(traps[1])

            traps.pop(0)
            traps.pop(0)
            traps.insert(0, merged_trap)


def case3(random_line: LineSegment, bounding_trapezoid_start: Trapezoid, bounding_trapezoid_end: Trapezoid, wall_start: Wall, wall_end: Wall, th: TrapezoidHolder, t: Tree, spanning_trapezoids: List[Trapezoid], ph: List[Point]):
    case1(random_line, bounding_trapezoid_start,
          bounding_trapezoid_end, wall_start, wall_end, th, t, ph)
    print("=================================================")
    print("After case 1 in case 3")
    print_traps(th)
    spanning_trapezoids = find_spanning_trapezoids_case_3(random_line, th)
    top_trapezoids: List[Trapezoid] = []
    bot_trapezoids: List[Trapezoid] = []
    plot_trapezoids_only(th)

    for trap in spanning_trapezoids:
        line_segment_left_point = Point(
            trap.top_line.point1.x, random_line.get_y_at(trap.top_line.point1.x))
        line_segment_right_point = Point(
            trap.top_line.point2.x, random_line.get_y_at(trap.top_line.point2.x))

        top_left = trap.top_line.point1
        top_right = trap.top_line.point2
        bot_left = trap.bot_line.point1
        bot_right = trap.bot_line.point2

        global trap_counter
        top_trapezoid = Trapezoid(
            Wall(top_left, line_segment_left_point,
                 trap.left_line.starting_point),
            Wall(top_right, line_segment_right_point,
                 trap.right_line.starting_point),
            LineSegment(top_left, top_right),
            LineSegment(line_segment_left_point, line_segment_right_point),
            "T"+str(trap_counter)
        )
        trap_counter += 1

        top_trapezoid = th.add_or_get_trapezoid(top_trapezoid)

        bot_trapezoid = Trapezoid(
            Wall(line_segment_left_point, bot_left,
                 trap.left_line.starting_point),
            Wall(line_segment_right_point, bot_right,
                 trap.right_line.starting_point),
            LineSegment(line_segment_left_point, line_segment_right_point),
            LineSegment(bot_left, bot_right),
            "T"+str(trap_counter)
        )
        trap_counter += 1

        bot_trapezoid = th.add_or_get_trapezoid(bot_trapezoid)


        if not top_trapezoid.is_zero_area():
            top_trapezoids.append(top_trapezoid)
        else:
            th.remove_trapezoid_from_lst(top_trapezoid)
        if not bot_trapezoid.is_zero_area():
            bot_trapezoids.append(bot_trapezoid)
        else:
            th.remove_trapezoid_from_lst(bot_trapezoid)


        # if not top_trapezoid.has_line(random_line) and not bot_trapezoid.has_line(random_line):
        if not top_trapezoid.is_zero_area() and not bot_trapezoid.is_zero_area():
            line_segment_copy = copy.deepcopy(random_line)
            line_segment_copy.left = top_trapezoid
            line_segment_copy.right = bot_trapezoid

            top_trapezoid.add_parent(line_segment_copy, Side.LEFT)
            bot_trapezoid.add_parent(line_segment_copy, Side.RIGHT)

            t.replace_trapezoid_with(trap, line_segment_copy)
            th.remove_trapezoid_from_lst(trap)

    plot_trapezoids_only(th)
    # merge mergeable trapezoids
    top_trapezoids.sort(key=lambda trap: trap.top_line.point1.x)
    bot_trapezoids.sort(key=lambda trap: trap.top_line.point1.x)

    merge_trapezoids(top_trapezoids, th)
    merge_trapezoids(bot_trapezoids, th)
    plot_trapezoids_only(th)
    print("here")


def plot_trapezoids_only(th: TrapezoidHolder):
    traps = th.get_trapezoids()

    fig, ax = plt.subplots()

    for trap in traps:
        plt.fill([
            trap.top_line.point1.x,
            trap.top_line.point2.x,
            trap.bot_line.point2.x,
            trap.bot_line.point1.x
        ], [
            trap.top_line.point1.y,
            trap.top_line.point2.y,
            trap.bot_line.point2.y,
            trap.bot_line.point1.y,
        ])

    plt.show()

def plot_trapezoids(th: TrapezoidHolder, line_segments: List[LineSegment]):
    traps = th.get_trapezoids()

    fig, ax = plt.subplots()

    for trap in traps:
        plt.fill([
            trap.top_line.point1.x,
            trap.top_line.point2.x,
            trap.bot_line.point2.x,
            trap.bot_line.point1.x
        ], [
            trap.top_line.point1.y,
            trap.top_line.point2.y,
            trap.bot_line.point2.y,
            trap.bot_line.point1.y,
        ])

    # plt.show()

    plot_lines((line_segments.values()), BoundingBox(0, 0, 100, 100), fig)


def createTree(line_segments: List[LineSegment], bounding_box, ph: List[Point]):
    temp_line_segments = list(line_segments.values())[:]
    th = TrapezoidHolder()
    # ph: List[Point] = []
    t = Tree(bounding_box)
    walls: List[Wall] = []

    # count = 0
    while len(temp_line_segments) > 0:
        line_segment = temp_line_segments.pop(0)

        bounding_trapezoid_start = t.find_boudning_trapezoid(
            line_segment.point1)
        bounding_trapezoid_end = t.find_boudning_trapezoid(line_segment.point2)

        # add bullets at start point to top and bottom line segments of bounding trapezoid
        top_y_start = bounding_trapezoid_start.top_line.get_y_at(
            line_segment.point1.x)
        bot_y_start = bounding_trapezoid_start.bot_line.get_y_at(
            line_segment.point1.x)

        wall_start_top = Point(line_segment.point1.x, top_y_start)
        wall_start_bot = Point(line_segment.point1.x, bot_y_start)
        wall_start: Wall = Wall(
            wall_start_top,
            wall_start_bot,
            line_segment.point1)

        # add bullets at end point to top and bottom line segments of bounding trapezoid
        top_x_end = bounding_trapezoid_end.top_line.get_x_at(
            line_segment.point2.y)
        bot_x_end = bounding_trapezoid_end.bot_line.get_x_at(
            line_segment.point2.y)
        wall_end_top = Point(top_x_end, line_segment.point2.y)
        wall_end_bot = Point(bot_x_end, line_segment.point2.y)
        wall_end: Wall = Wall(
            wall_end_top,
            wall_end_bot,
            line_segment.point2)

        replacement_node = None

        walls.append(wall_start)
        walls.append(wall_end)

        walls.sort(key=lambda line: line.point1.x)

        # case 2
        if bounding_trapezoid_start == bounding_trapezoid_end:
            case2(
                line_segment, bounding_trapezoid_start, bounding_trapezoid_end, wall_start, wall_end, th, t, ph)

        # case 1
        else:
            spanning_trapezoids = find_spanning_trapezoids(
                line_segment, th)
            if len(spanning_trapezoids) >= 1:
                case3(line_segment, bounding_trapezoid_start,
                      bounding_trapezoid_end, wall_start, wall_end, th, t, spanning_trapezoids, ph)
            else:
                case1(line_segment, bounding_trapezoid_start,
                      bounding_trapezoid_end, wall_start, wall_end, th, t, ph)

    print_traps(th)

    plot_trapezoids(th, line_segments)
    return t


def plot_lines(LineSegments: List[LineSegment], bounding_box: BoundingBox, fig=None):
    if fig is None:
        fig = plt.figure()

    for line in LineSegments:
        plt.plot([line.point1.x, line.point2.x],
                 [line.point1.y, line.point2.y], linewidth=3)
        plt.scatter(line.point1.x, line.point1.y, c="black")
        plt.scatter(line.point2.x, line.point2.y, c="black")
    plt.plot([bounding_box.left_line.point1.x, bounding_box.left_line.point2.x], [
             bounding_box.left_line.point1.y, bounding_box.left_line.point2.y])
    plt.plot([bounding_box.top_line.point1.x, bounding_box.top_line.point2.x], [
             bounding_box.top_line.point1.y, bounding_box.top_line.point2.y])
    plt.plot([bounding_box.right_line.point1.x, bounding_box.right_line.point2.x], [
             bounding_box.right_line.point1.y, bounding_box.right_line.point2.y])
    plt.plot([bounding_box.bot_line.point1.x, bounding_box.bot_line.point2.x], [
             bounding_box.bot_line.point1.y, bounding_box.bot_line.point2.y])

    plt.show()


def main():
    line_segments, bounding_box = read_input()
    ph = []

    for line in line_segments:
        ph.append(line_segments[line].point1)
        ph.append(line_segments[line].point2)
    plot_lines(list(line_segments.values())[:], bounding_box)
    t:Tree = createTree(line_segments, bounding_box, ph)

    inp = input("Enter point as x y")
    while inp != "quit":
        x, y = inp.strip().split()
        x, y = float(x), float(y)
        p = Point(x, y)

        print(t.find_boudning_trapezoid_path(p))
        inp = input("Enter point as x y")



if __name__ == "__main__":
    main()
