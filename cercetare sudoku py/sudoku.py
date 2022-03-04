print("COMPILING")
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
from utils import *
import sys
import sudoku_solve


img_path = os.path.join(sys.path[0], "images/app.jpg")
height = 450
width = 450

model = initialize_prediction_model("digit_model.h5")

### preprocesam imaginea/ thresholding ###
img = cv.imread(img_path)
img = cv.resize(img, (width, height))
img_thresh = pre_process(img)

### gasim contururile ###
img_contours = img.copy()
img_big_contour = img.copy()
contours, hierarchy = cv.findContours(img_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)#RETR_EXTERNAL ia doar conturul extern
cv.drawContours(img_contours, contours, -1, (0, 255, 0), 3)

### gasim cel mai mare contur ###
biggest, max_area = biggest_contour(contours)
if (biggest.size != 0):
    biggest = reorder(biggest)
    cv.drawContours(img_big_contour, biggest, -1, (0, 0, 255), 10)#se deseana cel mai mare contur
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    img_wrap_colored = cv.warpPerspective(img, matrix, (width, height))
    img_wrap_colored = cv.cvtColor(img_wrap_colored, cv.COLOR_BGR2GRAY)


    ### selectam fiecare cifra in parte ###
    boxes = split_boxes(img_wrap_colored)
    #cv.imshow("sample", boxes[0])
    nums = get_prediction(boxes, model)
    print(nums)
    img_detected_digits = img_wrap_colored.copy()#doar pt vizualizarea
    img_detected_digits = display_numbers(img_detected_digits, nums, color=(0, 255, 0))
    nums = np.asarray(nums)
    pos_arr = np.where(nums > 0, 0, 1)

    board = np.array_split(nums, 9)
    try:
        sudoku_solve.solve(board)
    except:
        pass

    flat_list = []
    for sublist in board:
        for item in sublist:
            flat_list.append(item)
    
    solved_nums = flat_list*pos_arr
    img_solved_digits = img_wrap_colored.copy()
    img_solved_digits = display_numbers(img_solved_digits, solved_nums)


#cv.imshow("Sudoku", img_thresh)
#cv.imshow("contours", img_contours)
#cv.imshow("big cont", img_big_contour)
cv.imshow("wraped", img_detected_digits)
cv.waitKey(0)