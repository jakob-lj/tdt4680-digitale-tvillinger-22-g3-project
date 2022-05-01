
import cv2


def makeImageSmallForReport(image):
    return cv2.resize(image, (500, 500), interpolation=cv2.INTER_AREA)
