from functions.utils import *


def process(img):
    doc = scan(img)

    kernel = np.ones((3, 3), np.uint8)
    doc = cv2.erode(doc, kernel, iterations=1)
    doc = cv2.dilate(doc, kernel, iterations=1)
    doc = padding(doc)

    return doc




