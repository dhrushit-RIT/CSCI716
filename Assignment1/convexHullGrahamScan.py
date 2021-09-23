import sys
from typing import final
from convexHullBruteForce import printPoints
import math


class Point:
    __slots__ = "x", "y"

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y


class LineSegment:
    __slots__ = "point1", "point2", "slope", "length"

    def hasPoint(self, point):
        return self.point1 == point or self.point2 == point

    def __init__(self, point1, point2) -> None:
        self.point1 = point1
        self.point2 = point2
        if point2.x != point1.x:
            self.slope = (point2.y - point1.y) / (point2.x - point1.x)
        else:
            self.slope = None
        self.length = math.sqrt(
            (point2.y - point1.y) * (point2.y - point1.y) + (point2.x - point1.x) * (point2.x - point1.x))

    def __eq__(self, o: object) -> bool:
        return (self.point1 == o.point1 and self.point2 == o.point2) or (
            self.point1 == o.point2 and self.point2 == o.point1)

    def __str__(self) -> str:
        return "<" + str(self.point1) + "-" + str(self.point2) + ">"


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


def readFromFile(filename):
    with open(filename) as f:
        numPoints = f.readline()
        points = []
        for line in f:
            line = line.strip()
            x, y = line.split()
            points.append(Point(float(x), float(y)))
    return points


def orientation(p, q, r):
    return q.x * r.y - r.x * q.y - p.x * r.y + p.x * q.y + r.x * p.y - q.x * p.y


def findUpperHull(points):
    upperPoints = []
    startPoint = points[0]
    endPoint = points[-1]
    minY = min(startPoint.y, endPoint.y)
    for point in points:
        if point.y >= minY:
            upperPoints.append(point)
    upperHull = []
    for i in range(3):
        if len(upperPoints) > 0:
            upperHull.append(upperPoints.pop(0))

    if len(upperHull) == 3:
        for point in upperPoints:
            while len(upperHull) >= 3 and orientation(upperHull[-3], upperHull[-2], upperHull[-1]) >= 0:
                upperHull.pop(-2)
            upperHull.append(point)
        while len(upperHull) >= 3 and orientation(upperHull[-3], upperHull[-2], upperHull[-1]) >= 0:
            upperHull.pop(-2)

    return upperHull


def findLowerHull(points):
    lowerPoints = []
    startPoint = points[0]
    endPoint = points[-1]
    minY = max(startPoint.y, endPoint.y)
    for point in points:
        if point.y <= minY:
            lowerPoints.append(point)
    lowerHull = []
    for i in range(3):
        if len(lowerPoints) > 0:
            lowerHull.append(lowerPoints.pop(0))

    if len(lowerHull) == 3:
        for point in lowerPoints:
            while len(lowerHull) >= 3 and orientation(lowerHull[-3], lowerHull[-2], lowerHull[-1]) <= 0:
                lowerHull.pop(-2)
            lowerHull.append(point)
        while len(lowerHull) >= 3 and orientation(lowerHull[-3], lowerHull[-2], lowerHull[-1]) <= 0:
            lowerHull.pop(-2)

    return lowerHull


def printPoints(points):
    for point in points:
        print(point, end=" ")
    print()


def printLines(lines):
    for line in lines:
        print(line)
    print()


def mergeHulls(lowerHull, upperHull):
    finalHull = lowerHull
    for point in reversed(upperHull[1:-1]):
        finalHull.append(point)
    return finalHull


def grahamScan(points):
    points = sorted(points, key=lambda point: point.x)

    upperHull = findUpperHull(points)
    # printPoints(upperHull)
    lowerHull = findLowerHull(points)
    # printPoints(lowerHull)
    finalHull = mergeHulls(lowerHull, upperHull)
    printPoints(finalHull)
    return finalHull


def divideConquerHull(points):
    pass


def writeToFile(filename, points):
    with open(filename, 'w') as f:
        f.write("number of points in the hull: "+str(len(points)) + "\n")
        for point in points:
            f.write(str(point) + "\n")


def main():
    filename = "points.txt"
    # filename = input("Enter name of the file:")
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    points = readFromFile(filename)
    hull_grahamScan = grahamScan(points)
    writeToFile("answer.txt", hull_grahamScan)


if __name__ == "__main__":
    main()
