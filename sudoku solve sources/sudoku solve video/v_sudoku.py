print("COMPILING")
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3' 

import cv2 as cv
import utils
import op_sudoku_solver as su

classifier = utils.init_model("digit_model.h5")

cap = cv.VideoCapture(0)
flag = 0

while True:

    ret, frame = cap.read()

    thresh = utils.preprocess(frame)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area, contour_grid = utils.find_biggest_contour(contours)

    if contour_grid is not None:
        cv.drawContours(frame, [contour_grid], 0, (0, 255, 0), 2)
        pts1, pts2 = utils.reorder_points(contour_grid)

        M = cv.getPerspectiveTransform(pts1, pts2)
        grid = cv.warpPerspective(frame, M, (utils.grid_size, utils.grid_size))
        grid = cv.cvtColor(grid, cv.COLOR_BGR2GRAY)
        grid = cv.adaptiveThreshold(grid, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 7, 3)

        cv.imshow("grid", grid)
        
        if flag == 0:
            grid_txt = utils.extract_sudoku_by_line(grid, classifier)
            print("\nPredicted rows from image:\n", grid_txt)
            print()
            result = su.sudoku(grid_txt)
        print("\nSolution:\n", result)

        if result is not None:
            flag = 1
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
            dst = cv.resize(dst, (1080, 620))
            cv.imshow("frame", dst)

        else:
            frame = cv.resize(frame, (1080, 620))
            cv.imshow("frame", frame)

    else:
        flag = 0
        frame = cv.resize(frame, (1080, 620))
        cv.imshow("frame", frame)

    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        break


cap.release()
cv.destroyAllWindows()