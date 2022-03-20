#importarea librariilor
import cv2 as cv
from keras.models import load_model
import numpy as np
import operator

# setarile specifice modelului de antrenare
# datele folosite la antrenarea modelului
# si sunt necesarea pentru identificarea cifrelor din imagine
margin = 4              # offsetul
cell = 28 + 2 * margin  # setarea latimii celulei din grila
                        # 28 - latimea&lungimea exemplelor de antrenare in baza de date
grid_size = 9 * cell    # setarea latimii unui rand din grila(sudoku)

# initierea modelului disponibil
def init_model(path):
    model = load_model(path) # functia de incarcare din keras
    return model

# prepocesarea imaginii pentru a putea fi prelucrata de model
def preprocess(img):
    # convertirea in imagine cu un singur canal gri
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # aplicarea blurului gaussian prin convolutia imaginii cu un nucleu 7x7
    gray = cv.GaussianBlur(gray, (7, 7), 0)
    # discretizarea(1 sau 0 pentru o anumita arie) imaginii prin aplicarea threshold-ului adaptiv
    thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 9, 2)
    return thresh

# gasirea celui mai mare contur din imagine
def find_biggest_contour(contours):
    max_area = 0
    contour_grid = None
    # bucla care parcurge toate contururile extrase
    for c in contours:
        # calcularea ariei
        area = cv.contourArea(c)
        # aplicarea filtrului pentru a evita contururile prea mici, considerate zgomote
        if (area > 25000):
            # calcularea perimetrului pentru contur (poligon inchis)
            peri = cv.arcLength(c, True)
            # aproximarea "laturilor" pologonului inchis
            polygone = cv.approxPolyDP(c, 0.01 * peri, True)
            # verificarea conditiei sa fie un dreptunghi & cel mai mare
            if (area > max_area and len(polygone) == 4):
                contour_grid = polygone
                max_area = area
    # returnarea ariei patratutului mare si conturul lui
    return max_area, contour_grid 

# rearanjarea ordinii punctelor colturilor patratului cu sudoku
def reorder_points(contour):
    # ierarhizarea contururilor vertical
    points = np.vstack(contour).squeeze()# se sterg toate array-urile de lungimea 1
    # sortarea punctelor din contur dupa al doilea parametru din array
    # itemgetter(1) extrage din obiect indexul a lui al doilea element
    points = sorted(points, key=operator.itemgetter(1))
    # reanjarea celor 4 coordonate de la stanga la dreapta, de jos si sus
    # se verifica sortarea x-urilor, deoarece a fost sortat dupa y
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
    # punctele care vor fi noi coordonate pentru cele extrase anterior
    pts2 = np.float32([[0, 0], [grid_size, 0], [0, grid_size], [grid_size, grid_size]])

    return pts1, pts2

# extragerea cifrelor din imagine, cate o linie
def extract_sudoku(grid, model):
    grid_txt = []
    # bulca pentru a extrage celulele din grila pentru prezicere
    for y in range(9):
        line = []
        for x in range(9):
            # setarile modelului antrenat, extragerea imaginii 
            # cu offset fara a se vedea marginile grilei
            y2min = y * cell + margin
            y2max = (y + 1) * cell - margin
            x2min = x * cell + margin
            x2max = (x + 1) * cell - margin
            # extragerea imaginii 28x28 cu toate offseturile din model
            img = grid[y2min:y2max, x2min:x2max]
            # salvarea imaginilor extrase pentru a putea fi vizualizate
            cv.imwrite("mat" + str(y) + str(x) + ".png", grid[y2min:y2max, x2min:x2max])
            # schimbarea formei array-ului pentru a putea fi prezis cifra
            # in rastrul de 28x28 folosit la prezicere de catre
            x = img.reshape(1, 28, 28, 1)
            # punerea filtrului adaugator pentru inlaturarea zgomotelor
            # x.sum() calculeaza suma in array, caci in x pixelul are sau 0 sau 255
            # deci suma pentru regiunea cu cifra va fi in jur de 15'000 - 20'000
            if(x.sum() > 10000):
                # efectuarea prezicerii prin functia din keras
                # matrice din 10 elemente unde probabilitatea 
                # se plaseaza la indexul care reflecta numarul prezis
                prediction = model.predict(x)
                # extragerea probabilitatii maxime pentru prezicere
                num_probability = np.amax(prediction)
                # filtru adaugator (nu e necesar, de obicei prob. = 100%)
                if(num_probability > 0.8):
                    # extragerea indexului cu cea mai mare valoare (probabilitate)
                    class_index = np.argmax(prediction, axis=-1)
                    # type casting in string
                    line.append(class_index[0]) # str(int(class_index[0]))
            else:# daca nu e prezent numarul atunci se atribuie 0
                line.append(0)
        # la lista de stringuri se ataseaza linia compusa
        grid_txt.append(line)
    
    return grid_txt

# functia de creare a noii imagini cu cifrele rezolvate inscrise
def put_numbers_on_blank(grid_txt, result):
    # crearea unei matrici de marimea grilei
    blank = np.zeros(shape=(grid_size, grid_size, 3), dtype=np.float32)
    for y in range(len(result)):
        for x in range(len(result[y])):
            # se pune raspunsul doar daca in grila originala acolo era 0
            if(grid_txt[y][x] == 0):
                cv.putText(blank, "{:d}".format(result[y][x]), ((x) * cell + margin + 3, 
                            (y + 1) * cell - margin - 3), cv.FONT_HERSHEY_DUPLEX, 0.9, (255, 0, 0), 1)
    return blank