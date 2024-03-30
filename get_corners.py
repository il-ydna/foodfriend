import cv2
import numpy as np

def clean_img(img):
    # convert img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    cv2.waitKey(0)

    # blur image
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    cv2.imshow('blur', blur)
    cv2.waitKey(0)

    # do otsu threshold on gray image
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    cv2.imshow('thresh', thresh)
    cv2.waitKey(0)

    #invert to make contours white
    invert = cv2.bitwise_not(thresh)
    processed = invert
    cv2.imshow('processed', processed)
    cv2.waitKey(0)
    return processed

def get_corners(img):
# read image
    # get largest contour
    contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    area_thresh = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > area_thresh:
            area_thresh = area
            big_contour = c
    # draw white filled largest contour on black just as a check to see it got the correct region
    page = np.zeros_like(img)
    cv2.drawContours(img, [big_contour], -1, (255,255,255), -1)
    cv2.imshow('img with contour', img)
    cv2.waitKey(0)

    cv2.drawContours(page, [big_contour], -1, (255,255,255), -1)
    cv2.imshow('just contour', page)
    cv2.waitKey(0)

    # get perimeter and approximate a polygon
    peri = cv2.arcLength(big_contour, True)
    corners = cv2.approxPolyDP(big_contour, 0.04 * peri, True)
    # draw polygon on input image from detected corners
    polygon = np.zeros_like(img)
    cv2.polylines(polygon, [corners], True, (255,255,255), 1, cv2.LINE_AA)
    cv2.imshow('polygon', polygon)
    cv2.waitKey(0)
    # Alternate: cv2.drawContours(page,[corners],0,(0,0,255),1)


    # print the number of found corners and the corner coordinates
    # They seem to be listed counter-clockwise from the top most corner
    res = np.zeros((4,2), dtype="float32")
    for i in range(4):
        res[i][0] = corners[i][0][0]
        res[i][1] = corners[i][0][1]
    print(corners)
    print(len(res))
    print(res)
    #POINTS ARE COUNTER CLOCKWISE FROM THE TOP MOST CORNER

    # for simplicity get average of top/bottom side widths and average of left/right side heights
    # note: probably better to get average of horizontal lengths and of vertical lengths
    width = 0.5*( (corners[0][0][0] - corners[1][0][0]) + (corners[3][0][0] - corners[2][0][0]) )
    height = 0.5*( (corners[2][0][1] - corners[1][0][1]) + (corners[3][0][1] - corners[0][0][1]) )
    width = np.intp(width)
    height = np.intp(height)

    return res

    #credit for corner identification
    #https://stackoverflow.com/questions/60941012/how-do-i-find-corners-of-a-paper-when-there-are-printed-corners-lines-on-paper-i
