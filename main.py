import numpy as np
import cv2
import os
import get_corners
import warp_image
import read_label


if __name__ == '__main__':
    img = cv2.imread(os.path.join("test", "test.png"))
    if img is None:
        print('Error opening image!')

    cleaned_img = get_corners.clean_img(img)
    rect = get_corners.get_corners(cleaned_img)

    warped_img = warp_image.four_point_transform(img, rect)
    cv2.imshow('image', warped_img)
    cv2.waitKey(0)

    readings = read_label.read_nutrition_facts(warped_img)

    print(read_label.parse_text(readings))



