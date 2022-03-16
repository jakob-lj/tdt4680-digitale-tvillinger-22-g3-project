
import cv2

from log import log


def detect(imagePath):
    log("Detecting image from: %s" % imagePath)

    img = cv2.imread(imagePath)

    cv2.imshow("Input", img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    cv2.imshow("HSV", hsv)

    print(img)
