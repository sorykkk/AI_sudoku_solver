import argparse
print("COMPILING")
import os
import sys
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3' 

#importarea tuturor dependentelor
import sudoku_solver as su
import utils     #from utils import * #asta pentru vizibilitate si distinctie mai buna
import cv2 as cv #din cauza importarii selective din utils nu se vor importa bibliotecile declarate acolo

#verificarea timpului de compilare
#import time 
#start_time = time.time()

#construim argument parser si extragem toate argumentele
#pentru folosirea mai comoda a CLI
ap = argparse.ArgumentParser()
ap.add_argument('-p', required=False, help="Specify the other(full) path to image")
args, leftovers = ap.parse_known_args()
default_img_path = "images/"

#salvarea locatiei fisierului
if(args.p is not None):
    print(args.p)
else:
    print(leftovers[0])
'''if(args['-p']):
    path = os.path.join(sys.path[0], args['-p'])###change it to console path
else:
    path = os.path.join(sys.path[0], default_img_path)

#citirea imaginei din locatie
frame = cv.imread(path)

#verificarea citirii corecte a imaginii
if(frame is None):
    print("###Incorrect path to image###")
    exit()

cv.imshow("frame", frame)'''
