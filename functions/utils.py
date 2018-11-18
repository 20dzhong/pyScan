
from functions.transform import *
from skimage.filters import threshold_local
import imutils

import cv2
import numpy as np


def cancel_noise(img):
    # blur and make image binary
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.bilateralFilter(img, 9, 75, 75)
    img = cv2.medianBlur(img, 5)

    upper = np.array([255])
    lower = np.array([170])

    mask = cv2.inRange(img, lower, upper)
    return mask


def resize(img):
    # resize to proportionally to 1120x800, if it doesn't fill, fill it with white space
    height, width = img.shape
    print(height, width)

    # ratio = list(map(int, str(Fraction(height, width)).split("/")))
    ratio = width/height
    n_height = round(800/ratio)
    n_width = round(1120*ratio)

    print(n_height, n_width)
    return img


def padding(img):
    row, col = img.shape[:2]
    bottom = img[row - 2:row, 0:col]
    mean = cv2.mean(bottom)[0]

    bordersize = 400
    border = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=[mean, mean, mean])

    return border


def scan(img):
    ratio = img.shape[0] / 500.0

    # save original so it doesnt get changed
    orig = img.copy()
    image = imutils.resize(img, height=500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cancel_noise(gray)

    binary = cv2.Canny(gray, 75, 200)

    # try:
    im2, cnts, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts = max(cnts, key=cv2.contourArea)
    # approximate the contour
    peri = cv2.arcLength(cnts, True)

    approx = cv2.approxPolyDP(cnts, 0.02 * peri, True)

    assert len(approx) == 4

    cv2.drawContours(image, cnts, -1, (0, 255, 0), 2)

    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(orig, approx.reshape(4, 2) * ratio)

    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > T).astype("uint8") * 255

    return warped

    # except:
    # print("Unacceptable photo, try taking another one!")