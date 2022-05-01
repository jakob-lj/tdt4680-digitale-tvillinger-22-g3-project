
import cv2


def makeImageSmallForReport(image):
    return cv2.resize(image, (0, 0), fx=0.1, fy=0.1)
