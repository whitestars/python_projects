import cv2
import numpy as np

image_origin = cv2.imread("F:/PycharmProjects/autoFQA/screenshot.png")
image_gray = cv2.cvtColor(image_origin, cv2.COLOR_BGR2GRAY)
image_template = cv2.imread("F:/PycharmProjects/autoFQA/question_pic.png")
print(image_template.shape, image_origin.shape, image_gray.shape)
h, w = image_template.shape[:-1]
methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
           cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
# cv2.imshow('rgb', image_origin)
# cv2.imshow('gray', image_gray)
# cv2.imshow('template',image_template)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


def methods_compare():
    for method in methods:
        res = cv2.matchTemplate(image_origin, image_template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0]+w, top_left[1]+h)
        cv2.rectangle(image_origin, top_left, bottom_right, (0, 255, 0), 2)
        win = cv2.namedWindow('test win', flags=0)
        cv2.imshow('test win', image_origin)
        print("result:", method)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def single_method():
    res = cv2.matchTemplate(image_origin, image_template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0]+w, top_left[1]+h)
    cv2.rectangle(image_origin, top_left, bottom_right, (0, 0, 255), 2)
    cv2.namedWindow("result", flags=0)
    cv2.imshow("result", image_origin)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


single_method()