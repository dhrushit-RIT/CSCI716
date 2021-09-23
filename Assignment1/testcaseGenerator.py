
import math
import random


def variationOfGiven(numPoints):
    points = [
        (10, 4),
        (7, 3),
        (8, 1),
        (6, -1),
        (9, -2),
        (11, -1),
        (12, 0),
        (15, 1),
        (14, 3),
        (13, 3),
    ]

    for row in range(0, 4):
        for col in range(8, 15):
            points.append((col, row))

    with open('test/variationOfGiven.txt', 'w') as f:

        f.write(str(len(points)) + "\n")
        for point in points:
            f.write(str(point[0]) + " " + str(point[1]) + "\n")


def allPointsOnSides(numPoints):
    filename = "test/" + str(numPoints) + "_allPointsOnSides.txt"
    width = math.floor(numPoints/4)
    height = math.ceil(numPoints/4)

    with open(filename, 'w') as f:
        f.write(str(numPoints) + "\n")
        for p in range(width):
            f.write("0 " + str(p) + "\n")
        for p in range(width):
            f.write(str(width-1) + " " + str(p) + "\n")
        for p in range(1, height-1):
            f.write(str(p) + " " + str(height-1) + "\n")
        for p in range(1, height-1):
            f.write(str(p) + " 0" + "\n")


def homogeneousSquares(numPoints):
    filename = "test/" + str(numPoints) + "_homogeneousSquares.txt"
    pointsPerScan = int(math.sqrt(numPoints))
    with open(filename, 'w') as f:
        f.write(str(numPoints) + "\n")
        for scanRow in range(pointsPerScan):
            for scanCol in range(pointsPerScan):
                f.write(str(scanRow) + " " + str(scanCol)+"\n")


def squareTests(numPoints):
    allPointsOnSides(numPoints)
    homogeneousSquares(numPoints)


def completelyRandom(numPoints):
    filename = "test/" + str(numPoints) + "_completelyRandom.txt"
    with open(filename, 'w') as f:
        f.write(str(numPoints) + "\n")
        for point in range(numPoints):
            f.write(str(random.randint(0, 100)) +
                    " "+str(random.randint(0, 100))+"\n")


def main():
    for numPoints in [10, 100, 1000, 10000, 100000]:
        variationOfGiven(numPoints)
        squareTests(numPoints)
        completelyRandom(numPoints)


if __name__ == "__main__":
    main()
