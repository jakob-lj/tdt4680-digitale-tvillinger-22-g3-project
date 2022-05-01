
import cv2


def makeImageSmallForReport(image):
    # return cv2.resize(image, (500, 500), interpolation=cv2.INTER_AREA)
    cropped = image[1800:3300, 1000:2500]
    return cv2.resize(cropped, (500, 500), interpolation=cv2.INTER_AREA)
