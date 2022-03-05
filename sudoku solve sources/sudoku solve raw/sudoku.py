print("COMPILING")
import os
import sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3' 

import sudoku_solver as su
import utils
import cv2 as cv 

import argparse

#import time 
#start_time = time.time()

ap = argparse.ArgumentParser()
ap.add_argument('-p', required=False, help="Specify the other(full) path to image")

args, leftovers = ap.parse_known_args()
default_img_path = "images/"

try:
    classifier = utils.init_model("digit_model.h5")
except:
    print("Error###The model cannot be loaded. Incorrect path to model###")
    exit()

if(args.p is not None):
    path = args.p
else:
    path = os.path.join(sys.path[0], default_img_path+leftovers[0])

frame = cv.imread(path)
if(frame is None):
    print("Error###Incorrect path to image###")
    exit()

thresh = utils.preprocess(frame)
contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)#retr_tree e pentru toate contururile
max_area, contour_grid = utils.find_biggest_contour(contours)

if (contour_grid is not None):
    cv.drawContours(frame, [contour_grid], 0, (0, 255, 0), 2)

    pts1, pts2 = utils.reorder_points(contour_grid)

    M = cv.getPerspectiveTransform(pts1, pts2)
    grid = cv.warpPerspective(frame, M, (utils.grid_size, utils.grid_size))
    grid = cv.cvtColor(grid, cv.COLOR_BGR2GRAY)
    grid = cv.adaptiveThreshold(grid, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 7, 3)#adaptive_thresh_gaussian_c folosit pentru cel mai bun thresh//detaliile se disting cel mai bine
    cv.imshow("grid", grid)

    grid_txt = utils.extract_sudoku_by_line(grid, classifier)

    print("\nPredicted rows from image:\n", grid_txt)
    print()
    result = su.sudoku(grid_txt)

    if (result is not None):
        print("\nSolution:\n", result)

        blank = utils.put_numbers_on_blank(grid_txt, result)

        M = cv.getPerspectiveTransform(pts2, pts1)
        h, w, c = frame.shape
        blankP = cv.warpPerspective(blank, M, (w, h))
        
        img2gray = cv.cvtColor(blankP, cv.COLOR_BGR2GRAY)
        ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
        mask = mask.astype('uint8')
        mask_inv = cv.bitwise_not(mask)

        img1_bg = cv.bitwise_and(frame, frame, mask=mask_inv)
        img2_fg = cv.bitwise_and(blankP, blankP, mask=mask).astype('uint8')
        dst = cv.add(img1_bg, img2_fg)
        #dst = cv.resize(dst, (650, 800))
        cv.imshow("frame", dst)

    else:
        #frame = cv2.resize(frame, (650, 800))
        cv.imshow("frame", frame)

else:
    #frame = cv2.resize(frame, (650, 800))
    cv.imshow("frame", frame)

#print(f"--- {(time.time()-start_time)} seconds ---")
cv.waitKey(0)