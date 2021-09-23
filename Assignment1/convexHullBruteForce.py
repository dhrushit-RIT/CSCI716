import sys
import math
import time

from util import Point
from util import LineSegment
from util import plotPointsAndHull


def getLowestPoint(points) -> Point:
    min_y_point = points[0]

    for point in points:
        if point.y < min_y_point.y:
            min_y_point = point
    return min_y_point


def sign(num):
    if num == 0:
        return 0
    elif num < 0:
        return -1
    else:
        return 1


def allPointsOnOneSide(point1, point2, points):
    # Line : y = mx + b
    # y - mx - b = 0 for all points on this line
    # y - mx - b < 0 for points on left
    # y - mx - b > 0 for points on right
    if point2.x != point1.x:
        slope = (point2.y - point1.y) / (point2.x-point1.x)
    else:
        slope = None
    if slope != None:
        y_intercept = point1.y - slope * point1.x
    else:
        y_intercept = None

    side = 0

    for point in points:  # O(n)
        if point != point1 and point != point2:
            if slope != None:
                pointSide = sign(point.y - slope * point.x -
                                 y_intercept)  # O(1)
            else:
                if point.x > point1.x:
                    pointSide = 1
                elif point.x == point1.x:
                    pointSide = 0
                else:
                    pointSide = -1
            if side == 0:
                side = pointSide
            else:
                if pointSide != 0 and pointSide != side:
                    return False
                else:
                    continue
    return True


def bruteForce(points):
    print("finding answer to life universe and everything")
    hullLines = []
    for point1 in points:
        for point2 in points:
            if point1 != point2:
                # print("point1", point1, "point2", point2)
                if allPointsOnOneSide(point1, point2, points):
                    lineSegment = LineSegment(point1, point2)
                    if lineSegment not in hullLines:
                        hullLines.append(lineSegment)
                else:
                    # print("all points on either side")
                    continue

    return hullLines


def readFromFile(filename):
    with open(filename) as f:
        numPoints = f.readline()
        points = []
        for line in f:
            line = line.strip()
            x, y = line.split()
            points.append(Point(float(x), float(y)))
    return points


def printPoints(points):
    for point in points:
        print(point, end=" ")
    print()


def printLines(lines, tag):
    if tag:
        print(tag)
    for line in lines:
        print(line)
    print()


def orderLines(lines):
    print("orderign lines:")
    sequencedLines = [lines[0]]
    firstLine = lines[0]
    lines.pop(0)
    while True:
        lastLine = sequencedLines[-1]
        if len(sequencedLines) > 1 and lastLine.hasPoint(firstLine.point1):
            break
        else:
            nextLine = None
            for line in lines:
                if line.hasPoint(lastLine.point2) and line != lastLine:
                    if line.point1 != lastLine.point2:
                        line.swapPoints()
                    sequencedLines.append(line)
                    lines.remove(line)
                    break
            # if sequencedLines[-1] in lines:
            #     lines.remove(sequencedLines[-1])
    return sequencedLines


def getPointsFromLines(lines):
    """
        pre: the lines are ordered in a sequence and lines has at least 3 points
    """
    print("fetching points from the lines")
    points = []
    if lines[1].point1 == lines[0].point1 or lines[1].point2 == lines[0].point1:
        points.append(lines[0].point2)
        points.append(lines[0].point1)

    else:
        points.append(lines[0].point1)
        points.append(lines[0].point2)

    for line in lines[1:-1]:
        if line.point1 == points[-1]:
            points.append(line.point2)
        else:
            points.append(line.point1)
    return points


def deleteCollinearLines(lines):
    print("deleting collinear lines")
    linesToRemove = []
    nonCollinearLines = []
    for line1 in lines:
        for line2 in lines:
            if line1 != line2:
                if line1.slope == line2.slope:
                    if line2.hasPoint(line1.point1) or line2.hasPoint(line1.point2):
                        if line1.length < line2.length:
                            if line1 not in linesToRemove:
                                linesToRemove.append(line1)

    for line in linesToRemove:
        lines.remove(line)

    return lines


def writeToFile(filename, points):
    print("writing to file")
    with open(filename, 'w') as f:
        f.write(str(len(points)) + "\n")
        for point in points:
            f.write(str(point) + "\n")


def orientation(p, q, r):
    return q.x * r.y - r.x * q.y - p.x * r.y + p.x * q.y + r.x * p.y - q.x * p.y


def makeCounterClockwise(points):
    if orientation(points[0], points[1], points[2]) < 0:
        points.reverse()
    return points


def main():
    filename = "points.txt"
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    points = readFromFile(filename)
    start_time = time.time()
    hull_bruteForce = bruteForce(points)  # all points on one side of the line
    end_time = time.time()
    hull_find_time = end_time - start_time

    start_time = time.time()
    nonCollinearLines = deleteCollinearLines(hull_bruteForce)
    orderedLines = orderLines(nonCollinearLines)
    hullPoints = getPointsFromLines(orderedLines)

    ccwPoints = makeCounterClockwise(hullPoints)
    end_time = time.time()
    post_process_time = end_time-start_time
    printPoints(ccwPoints)
    writeToFile("answer.txt", ccwPoints)

    print("time to find hull:", hull_find_time)
    print("time to post process(sequence, order etc):", post_process_time)

    plotPointsAndHull(points, ccwPoints)


if __name__ == "__main__":
    main()
