
import cv2

from imageProcessing.crosswalkDetection import detect

if __name__ == '__main__':
    # detect("assets/mock/small_crosswalk_ok_shape.png")
    detect("output.tif", outputImages=True)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
