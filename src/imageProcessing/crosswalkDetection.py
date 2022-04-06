
import cv2
import numpy as np

from log import log


def detect(imagePath, useFirstPersonView=False):
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
    lowerWhite = np.array([0, 240, 0])
    upperWhite = np.array([225, 255, 255])

    rectangleMask = np.zeros(img.shape[:2], dtype="uint8")
    height = img.shape[0]
    width = img.shape[1]

    cv2.rectangle(rectangleMask, (0, int(height/2)), (width, height), 255, -1)

    hlsMask = cv2.inRange(hls, lowerWhite, upperWhite)

    # TODO: bitwise_and for masks in order to not bitwise image twice
    masked = cv2.bitwise_and(img, img, mask=hlsMask)
    if (useFirstPersonView):
        masked = cv2.bitwise_and(masked, masked, mask=rectangleMask)

    # Disclaimer - a little of this is copied from : https://www.delftstack.com/howto/python/opencv-detect-rectangle/ :)
    gray_img = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

    thresh_img = cv2.threshold(
        gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # cv2.imshow("trash", thresh_img)

    coloredThresCopy = cv2.cvtColor(thresh_img, cv2.COLOR_BAYER_BG2BGR)

    cnts = cv2.findContours(
        thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    rectList = []

    for cnt in cnts:
        approx = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        approxy = cv2.approxPolyDP(cnt, 0.015 * peri, True)
        if len(approxy) == 4:
            x, y, w, h = cv2.boundingRect(approxy)
            rectList.append((x, y, w, h))

            cv2.rectangle(coloredThresCopy, (x, y),
                          (x+w, y+h), (36, 255, 12), 2)

        if(approx > 1000):  # 300 seems like a good approximation for the size of a crosswalk element
            approximations.append(approx)
            for i in range(len(cnt[:-1])):
                start = cnt[i][0]
                end = cnt[i+1][0]

                # Draw the lines between contour elements to display them
                cv2.line(coloredThresCopy, start, end, (0, 0, 225), 3)

    # Group threshold holds the number of rectangles should be grouped
    print(rectList)
    # Grouping rectangles does not work as of now
    print(cv2.groupRectangles(rectList=rectList, groupThreshold=3))

    cv2.imshow("Result", coloredThresCopy)

    cv2.imwrite("results/crosswalk_detection.png", img)
