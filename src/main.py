
import sys
# import cv2
from stringHelpers import bold, green


def log(message):
    """
    Helper function to log messages - used in order to support
    hard core logging at a later point of view
    """

    print(message)


class Images:
    """
    Helper class in order to define the default images used in order to
    demonstrate alorithm.

    All dataset used should have these images. Look at asssets/mock/ in order
    to see sample images.

    Size does not matter.
    """

    NO_CROSSWALK = "no_crosswalk"
    CROSSWALK_OK_SHAPE = "small_crosswalk_ok_shape"


SUPPORTED_IMAGES = [Images.NO_CROSSWALK, Images.CROSSWALK_OK_SHAPE]


def defineImages(mocking):
    """
    Helper method used in order to read image paths from a dataset
    into memory based on runtime attributes.
    """

    global images
    if (mocking):
        images = {
            Images.NO_CROSSWALK: "assets/mock/no_crosswalk.png",
            Images.CROSSWALK_OK_SHAPE: "assets/mock/small_crosswalk_ok_shape.png"
        }
    else:
        raise "Missing data from Terratec"


def stringifyFlags(mocking):
    """
    Helper method to log what flags are precent
    """

    return "%s: %s\n" % (green("--mocking"), mocking)


def stringigyImages(images):
    """
    Helper method to log what images is being used
    """

    result = []
    for imageType in SUPPORTED_IMAGES:
        result.append("%s - %s" % (green(imageType), (images[imageType])))

    return "\n".join(result)


if __name__ == '__main__':
    if not "--mocking" in sys.argv:
        mocking = False
    else:
        mocking = True

    defineImages(mocking)

    log("%s\n%s" % (bold("Running with flags"), stringifyFlags(mocking)))

    log("%s\n%s" % (bold("Running with image set:"), stringigyImages(images)))
