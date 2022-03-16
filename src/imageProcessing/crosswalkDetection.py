
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

    log("Detecting image from: %s" % imagePath)

    img = cv2.imread(imagePath)

    cv2.imshow("Input", img)

    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    cv2.imshow("HLS", hls)

    # define range of blue color in HLS
    lowerWhite = np.array([0, 140, 0])
    upperWhite = np.array([225, 255, 255])

    # Threshold the HLS image to get only white colors
    mask = cv2.inRange(hls, lowerWhite, upperWhite)

    # Bitwise-AND mask and original image
    masked = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("Masked image", masked)

    gray_img = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

    cv2.imshow("gray", gray_img)
    thresh_img = cv2.threshold(
        gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(
        thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for cnt in cnts:
        # print(cnt)
        approx = cv2.contourArea(cnt)
        print(approx)
        for i in range(len(cnt[:-1])):
            start = cnt[i][0]
            end = cnt[i+1][0]
            print(start, end)
            # cv2.line(img, (coords[0], coords[1]), (225, 0, 0), 3)

            # print(x)
            pass
        break

    cv2.imshow("binary", thresh_img)
