import cv2 as cv
from keras.models import load_model
import numpy as np
import operator

margin = 4
cell = 28 + 2 * margin
grid_size = 9 * cell

def init_model(path):
    model = load_model(path)
    return model

def preprocess(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (7, 7), 0)
    thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 9, 2)
    return thresh

def find_biggest_contour(contours):
    max_area = 0
    contour_grid = None
    for c in contours:
        area = cv.contourArea(c)
        if (area > 25000):
            peri = cv.arcLength(c, True)
            polygone = cv.approxPolyDP(c, 0.01 * peri, True)
            if (area > max_area and len(polygone) == 4):
                contour_grid = polygone
                max_area = area
                
    return max_area, contour_grid 

def reorder_points(contour):
    points = np.vstack(contour).squeeze()# se sterg toate array-urile de lungimea 1
    points = sorted(points, key=operator.itemgetter(1))
    if(points[0][0] < points[1][0]):
        if(points[3][0] < points[2][0]):
            pts1 = np.float32([points[0], points[1], points[3], points[2]])
        else:
            pts1 = np.float32([points[0], points[1], points[2], points[3]])
    else:
        if(points[3][0] < points[2][0]):
            pts1 = np.float32([points[1], points[0], points[3], points[2]])
        else:
            pts1 = np.float32([points[1], points[0], points[2], points[3]])

    pts2 = np.float32([[0, 0], [grid_size, 0], [0, grid_size], [grid_size, grid_size]])

    return pts1, pts2

def extract_sudoku(grid, model):
    grid_txt = []
    for y in range(9):
        line = []
        for x in range(9):
            y2min = y * cell + margin
            y2max = (y + 1) * cell - margin
            x2min = x * cell + margin
            x2max = (x + 1) * cell - margin
            
            img = grid[y2min:y2max, x2min:x2max]
            cv.imwrite("mat" + str(y) + str(x) + ".png", img)
            x = img.reshape(1, 28, 28, 1)
            
            if(x.sum() > 10000):
                prediction = model.predict(x)
                num_probability = np.amax(prediction)
                if(num_probability > 0.8):
                    class_index = np.argmax(prediction, axis=-1)
                    line.append(class_index[0]) # str(int(class_index[0]))
            else:
                line.append(0)

        grid_txt.append(line)
    
    return grid_txt

def put_numbers_on_blank(grid_txt, result):
    blank = np.zeros(shape=(grid_size, grid_size, 3), dtype=np.float32)
    for y in range(len(result)):
        for x in range(len(result[y])):
            if(grid_txt[y][x] == 0):
                cv.putText(blank, "{:d}".format(result[y][x]), ((x) * cell + margin + 3, 
                            (y + 1) * cell - margin - 3), cv.FONT_HERSHEY_DUPLEX, 0.9, (255, 0, 0), 1)
    return blank