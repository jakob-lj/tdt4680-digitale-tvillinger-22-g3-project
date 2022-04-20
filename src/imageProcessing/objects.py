import numpy as np

from geometrics import calculateDistance


def crossWalkIFy(crossWalkRectangles):
    return Crosswalk(crossWalkRectangles)


class Rectangle:
    def __init__(self, leftUpperCornerX, leftUpperCornerY, w, h):
        self.leftUpperCornerX = leftUpperCornerX
        self.leftUpperCornerY = leftUpperCornerY
        self.w = w
        self.h = h

    def getCenter(self):
        return (int(self.leftUpperCornerX + (self.w/2)), int(self.leftUpperCornerY + (self.h/2)))

    def getLargestSize(self):
        return max(self.w, self.h)

    def getLeftPoint(self):
        return self.leftUpperCornerX

    def getRightPoint(self):
        return self.leftUpperCornerX + self.w

    def getTopPoint(self):
        return self.leftUpperCornerY

    def getBottomPoint(self):
        return self.leftUpperCornerY + self.h


class Crosswalk:

    def _getCorners(self):

        maxLeftPoint = np.inf
        maxRightPoint = 0
        maxTopPoint = np.inf
        maxBottomPoint = 0

        for rect in self.rectangles:
            if (rect.getLeftPoint() < maxLeftPoint):
                maxLeftPoint = rect.getLeftPoint()

            if (rect.getRightPoint() > maxRightPoint):
                maxRightPoint = rect.getRightPoint()

            if (rect.getTopPoint() < maxTopPoint):
                maxTopPoint = rect.getTopPoint()

            if (rect.getBottomPoint() > maxBottomPoint):
                maxBottomPoint = rect.getBottomPoint()

        """
        Points in current order
        
        1---------4
        |         |
        |         |
        2---------3
        """

        return ((maxLeftPoint, maxTopPoint), (maxLeftPoint, maxLeftPoint), (maxRightPoint, maxBottomPoint), (maxRightPoint, maxTopPoint))

    def _getCenter(self):
        sumX = 0
        sumY = 0
        for element in self.rectangles:
            center = element.getCenter()
            sumX += center[0]
            sumY += center[1]

        return (int(sumX / len(self.rectangles)), int(sumY / len(self.rectangles)))

    def __init__(self, rectangles):
        self.rectangles = rectangles

        self.corners = self._getCorners()

        self.center = self._getCenter()

        self.upperLeftCorner = self.corners[0]

        self.upperRightCorner = self.corners[3]

        self.lowerLeftCorner = self.corners[1]

        self.lowerRightCorner = self.corners[2]

        self.width = max(calculateDistance(
            self.upperLeftCorner, self.upperRightCorner),
            calculateDistance(self.lowerLeftCorner, self.lowerRightCorner))

        self.height = max(calculateDistance(self.lowerLeftCorner, self.upperLeftCorner),
                          calculateDistance(self.lowerRightCorner, self.upperRightCorner))
