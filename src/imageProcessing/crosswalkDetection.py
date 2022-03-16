
import cv2
import numpy as np

from log import log


def detect(imagePath):
    """

    Cross walk detection using HLS filters. 
    In order to find crosswalk. 

    Us HLS (hue, lightness, saturation) for white filtering as white (seen as light) 
    seems to be a good masking option.
    """

    approximations = []

    log("Detecting image from: %s" % imagePath)

    img = cv2.imread(imagePath)

    # cv2.imshow("Input", img)

    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # cv2.imshow("HLS", hls)

    # define range of blue color in HLS
    lowerWhite = np.array([0, 140, 0])
    upperWhite = np.array([225, 255, 255])

    rectangleMask = np.zeros(img.shape[:2], dtype="uint8")
    height = img.shape[0]
    width = img.shape[1]

    cv2.rectangle(rectangleMask, (0, int(height/2)), (width, height), 255, -1)

    hlsMask = cv2.inRange(hls, lowerWhite, upperWhite)

    # TODO: bitwise_and for masks in order to not bitwise image twice
    masked = cv2.bitwise_and(img, img, mask=hlsMask)
    masked = cv2.bitwise_and(masked, masked, mask=rectangleMask)

    # Disclaimer - a little of this is copied from : https://www.delftstack.com/howto/python/opencv-detect-rectangle/ :)
    gray_img = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

    thresh_img = cv2.threshold(
        gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(
        thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for cnt in cnts:
        approx = cv2.contourArea(cnt)

        if(approx > 300):  # 300 seems like a good approximation for the size of a crosswalk element
            approximations.append(approx)
            for i in range(len(cnt[:-1])):
                start = cnt[i][0]
                end = cnt[i+1][0]

                # Draw the lines between contour elements to display them
                cv2.line(img, start, end, (0, 0, 225), 3)

    cv2.imshow("Result", img)

    cv2.imwrite("results/crosswalk_detection.png", img)
