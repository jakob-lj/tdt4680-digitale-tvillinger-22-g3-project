
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
