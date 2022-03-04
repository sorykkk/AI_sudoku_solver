#ifndef _IMAGE_H_
#define _IMAGE_H_

#include <opencv2/opencv.hpp>

#include "OCR.h"

using namespace std;
using namespace cv;

//ratia cazului/numar intr-un caz
const int case_size = matching_size * 1.6;

//mareste cazul/marimea numarului in timp ce se selecteaza cazul/numar
const int crop_size = matching_size * 0.3;

int displayImage(const String display_name, Mat img);
Mat processInput(Mat img);
void transformScrabble(Mat img_src, Mat& img_tr, Rect& big_rect);
void segmentSudoku(Mat img, Mat& img_num, int x, int y);
void drawSudoku(Mat img, Rect rect, int grid[9][9]);

#endif