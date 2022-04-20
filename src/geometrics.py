
from audioop import cross
import math


def calculateDistance(pointA, pointB):

    (xA, yA) = pointA
    (xB, yB) = pointB

    x = (xA - xB)
    y = (yA - yB)

    return math.sqrt(x**2 + y**2)


def crossWalkIFy(crossWalkRectangles):
    return crossWalkRectangles
