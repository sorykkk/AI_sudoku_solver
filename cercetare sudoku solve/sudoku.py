# Curatarea ecranului consolei de toate mesajele de avertizare a librarii tensorflow
print("COMPILING")
import os
import sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3' 

# importarea tuturor dependentelor
import sudoku_solver as su
import utils     # from utils import * #asta pentru vizibilitate si distinctie mai buna
import cv2 as cv # din cauza importarii selective din utils nu se vor importa bibliotecile declarate acolo

import argparse  # librarie pentru procesarea argumentelor introduse in consola

# verificarea timpului de compilare
#import time 
#start_time = time.time()

# construim argument parser si extragem toate argumentele
# pentru folosirea mai comoda a CLI
ap = argparse.ArgumentParser()
ap.add_argument('-p', required=False, help="Specify the other(full) path to image")
# separam argumentele indicate de cele care nu au argument
args, leftovers = ap.parse_known_args()
default_img_path = "images/"

# verificarea importarii corecte a modelului antrenat
try:
    classifier = utils.init_model("digit_model.h5")
except:
    print("Error###The model cannot be loaded. Incorrect path to model###")
    exit()

# salvarea locatiei fisierului
# daca este specificat argumentul atunci se va deschide imaginea din locatia indicata
# -p pentru indicarea completa a locatiei imaginei
if(args.p is not None):
    path = args.p
else:# daca nu se indica atunci se vor deschide imaginea din fisierul <images>
    path = os.path.join(sys.path[0], default_img_path+leftovers[0])

# citirea imaginei din locatie
frame = cv.imread(path)

# verificarea citirii corecte a imaginii
if(frame is None):
    print("Error###Incorrect path to image###")
    exit()

# aplicarea thresholdingului
thresh = utils.preprocess(frame)
# extragerea tuturor contururilor
contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)#retr_tree e pentru toate contururile

# aflarea ariei maxime(ce va reprezenta conturul sudoku care trebuie rezolvat)
# si conturul ce apartine acestei arii
max_area, contour_grid = utils.find_biggest_contour(contours)

# verificam daca a fost gasit conturul
if (contour_grid is not None):
    # desenarea conturulului pe imaginea originala
    cv.drawContours(frame, [contour_grid], 0, (0, 255, 0), 2)
    
    # pts1 - rearanjarea intr-o ordine specifica a colturilor conturului
    # pts2 - punctele folosite pentru perspectiva
    pts1, pts2 = utils.reorder_points(contour_grid)

    # aratam grila pentru a vedea sursa
    # aplicam perspectiva asupra imaginii
    M = cv.getPerspectiveTransform(pts1, pts2)
    # extragerea imaginii cu perspectiva modificata
    grid = cv.warpPerspective(frame, M, (utils.grid_size, utils.grid_size))
    grid = cv.cvtColor(grid, cv.COLOR_BGR2GRAY)
    grid = cv.adaptiveThreshold(grid, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 7, 3)#adaptive_thresh_gaussian_c folosit pentru cel mai bun thresh//detaliile se disting cel mai bine
    cv.imshow("grid", grid)
    # extragerea fiecarui rand a sudoku
    grid_txt = utils.extract_sudoku_by_line(grid, classifier)

    # afisarea in consola randurilor extrase
    print("\nPredicted rows from image:\n", grid_txt)
    print()
    # rezolvarea sudoku si returnarea rezultatului in forma de matrice 2x2
    # fara modificarea matricei de stringuri grid_txt
    result = su.sudoku(grid_txt)

    # daca a fost gasita solutia la sudoku
    if (result is not None):
        print("\nSolution:\n", result)
        # crearea unei imagini goale doar cu numerele rezolvate inserate
        blank = utils.put_numbers_on_blank(grid_txt, result)
        # transformarea in perspectiva originala a imaginii din pts1 in pts2
        M = cv.getPerspectiveTransform(pts2, pts1)
        h, w, c = frame.shape
        blankP = cv.warpPerspective(blank, M, (w, h))# aplicarea perpectivei la imagine
        
        # creeam masca textului care trebuie inserat si inversul mastii
        img2gray = cv.cvtColor(blankP, cv.COLOR_BGR2GRAY)
        # discretizeaza imaginea
        # la micsorarea parametrului thresh se mareste aria unde se aplica threshold-ul
        # adica aria unde mai multe valori intermediare pot primi valoarea 1 ci nu 0
        ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
        mask = mask.astype('uint8')
        # seteaza inversului mastii discretizate
        mask_inv = cv.bitwise_not(mask)

        # intunecarea ariei in imaginea originala pt amplasarea cifrelor
        img1_bg = cv.bitwise_and(frame, frame, mask=mask_inv)
        # se ia doar regiunea cu cifrele din blankP (adica doar 
        # regiunile care au thresholdul setat [1])
        img2_fg = cv.bitwise_and(blankP, blankP, mask=mask).astype('uint8')
        # se pune img2_fg (imaginea cu cifrele) pe imaginea
        # originala, modificand-o
        dst = cv.add(img1_bg, img2_fg)
        # modificarea marimii imaginii ce se va afisa
        #dst = cv.resize(dst, (650, 800))
        cv.imshow("frame", dst)

    else: # daca nu se poate rezolva
        #frame = cv2.resize(frame, (650, 800))
        # se afiseaza doar imaginea cu conturul evidentiat
        cv.imshow("frame", frame)

else: # daca nu s-a gasit conturul
    #frame = cv2.resize(frame, (650, 800))
    # se afiseaza doar imaginea originala fara contur
    cv.imshow("frame", frame)

# afisarea timpului de compilare totala
#print(f"--- {(time.time()-start_time)} seconds ---")

cv.waitKey(0)