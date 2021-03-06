
from turtle import color
import cv2
import numpy as np
from geometrics import calculateDistance
from imageProcessing.imageProcess import makeImageSmallForReport
from imageProcessing.objects import Rectangle, crossWalkIFy

from log import log
from tifHandlers.coordinateConverter import convertPixelPlacementToCoordinates


def groupRectanglesToCrossWalks(rectangles, distanceThreshold=0.2):
    """
    distanceThreshold is the decimal ratio between length of crosswalk and distance to another crosswalk
    thats acceptable to be in a group of crosswalk elements => a crosswalk

    This function will take the center of each rectangle and calculate the distance to other rectangles grouping them
    into lists of rectangles that are inside the ratio of another rectangle in the group.
    """

    groups = []
    currentRectangle = rectangles[0]
    groups.append([currentRectangle])

    def getGroupOfRectangle(rect):
        for g in groups:
            if(rect in g):
                return g

        return None

    def mergeGroups(group1, gruop2):
        print("Merging gruops")
        raise "Merging crosswalk groups is currently not implemented"

    def groupRectangles(rect1, rect2):
        groupOfRect1 = getGroupOfRectangle(rect1)
        groupOfRect2 = getGroupOfRectangle(rect2)

        if (groupOfRect1 == None and groupOfRect2 == None):  # create new group
            groups.append([rect1, rect2])

        elif (groupOfRect1 != None and groupOfRect2 == None):  # rect 1 has group, not 2
            groupOfRect1.append(rect2)

        elif (groupOfRect2 != None and groupOfRect1 == None):
            groupOfRect2.append(rect1)

        elif (groupOfRect2 != None and groupOfRect1 != None):
            if (groupOfRect1 == groupOfRect2):  # They already are in the same group, skip
                pass
            else:
                # the gruops should be merged
                mergeGroups(groupOfRect1, groupOfRect1)

    # exclude first as it already has a group
    for outerRectangleIndex in range(len(rectangles))[1:]:
        currentRectangle = rectangles[outerRectangleIndex]

        for innerRectangleIndex in range(len(rectangles)):
            if (outerRectangleIndex == innerRectangleIndex):  # don't calculate for the same element
                continue

            naborRectangle = rectangles[innerRectangleIndex]

            distance = calculateDistance(currentRectangle.getCenter(
            ), naborRectangle.getCenter())

            largestThreshold = max(
                currentRectangle.getLargestSize(), naborRectangle.getLargestSize())

            if (distance < largestThreshold):
                groupRectangles(currentRectangle, naborRectangle)

    return [crossWalkIFy(group) for group in groups]


def detect(imagePath, outputImages=False, useFirstPersonView=False):
    """

    Cross walk detection using HLS filters.
    In order to find crosswalk.

    Us HLS (hue, lightness, saturation) for white filtering as white (seen as light)
    seems to be a good masking option.

    useFirstPersonView was implemented in order to filter out heaven from google maps images
    and is currently not in use for terratec images
    """

    approximations = []

    log("Detecting image from: %s" % imagePath)

    img = cv2.imread(imagePath)

    # cv2.imshow("Input", img)

    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # cv2.imshow("HLS", hls)
    cv2.imwrite("results/HLS.png", makeImageSmallForReport(hls))

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

    cv2.imwrite("results/gray.png", makeImageSmallForReport(gray_img))

    thresh_img = cv2.threshold(
        gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # cv2.imshow("trash", thresh_img)

    cv2.imwrite("results/masked_image.png",
                makeImageSmallForReport(thresh_img))

    coloredThresCopy = cv2.cvtColor(thresh_img, cv2.COLOR_BAYER_BG2BGR)

    cnts = cv2.findContours(
        thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    rectanglesList = []

    for cnt in cnts:
        approx = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        approxy = cv2.approxPolyDP(cnt, 0.015 * peri, True)
        if len(approxy) == 4:
            x, y, w, h = cv2.boundingRect(approxy)

            if (approx > 1000):
                objectRepresentation = Rectangle(x, y, w, h)
                rectanglesList.append(objectRepresentation)
                # cv2.rectangle(coloredThresCopy, (x, y),
                #               (x+w, y+h), (36, 255, 12), 2)

        if(approx > 1000):  # 300 seems like a good approximation for the size of a crosswalk element
            approximations.append(approx)
            for i in range(len(cnt[:-1])):
                start = cnt[i][0]
                end = cnt[i+1][0]

                # Draw the lines between contour elements to display them
                cv2.line(coloredThresCopy, start, end, (0, 0, 225), 3)

    cv2.imwrite("results/withrectangles.png",
                makeImageSmallForReport(coloredThresCopy))

    # Group threshold holds the number of rectangles should be grouped
    # Grouping rectangles does not work as of now
    # print(cv2.groupRectangles(rectList=rectList, groupThreshold=3))

    crossWalkGroups = groupRectanglesToCrossWalks(rectanglesList)

    outputImg = img

    font = cv2.FONT_HERSHEY_SIMPLEX
    for crosswalk in crossWalkGroups:
        # print(crosswalk)
        # print(crosswalk.center)
        cv2.circle(outputImg, crosswalk.center, 15, (255, 0, 0),  -1)
        # print(crosswalk.corners)

        cv2.rectangle(outputImg, crosswalk.upperLeftCorner,
                      crosswalk.lowerRightCorner, (0, 0, 255), 2)

        crosswalkCoordinates = convertPixelPlacementToCoordinates(
            imagePath, crosswalk.center)

        coordiantesText = "%s" % str(crosswalkCoordinates)

        cv2.imwrite("results/crosswalk_witout_position.png",
                    makeImageSmallForReport(outputImg))

        cv2.putText(outputImg, coordiantesText,
                    (crosswalk.lowerLeftCorner[0] - 460, crosswalk.lowerRightCorner[1]+70), font, 2, (0, 0, 225), 2, cv2.LINE_AA)

    if (len(crossWalkGroups) > 0):
        log("Crosswalk has been detected in %s" %
            [x.split("/") for x in imagePath.split("\\")][-1][0])

    if(outputImages):
        cv2.imshow("Result", outputImg)

    cv2.imwrite("results/crosswalk_detection.png",
                makeImageSmallForReport(outputImg))

    return crossWalkGroups
