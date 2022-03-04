#ifndef _OCR_H_
#define _OCR_H_

#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;
using namespace cv::ml;

//inaltimea minima in pixeli pentru train data de input
const int train_height_min = 9;

//potrivirea marimea pixelilor patratului OCR
const int matching_size = 35;

//distanta minima de potrivire pentru a rezolva un numar
const int minimum_matching_dist = 10e7;

void trainOCR(String filename, Mat& sample, Mat& response);
void loadTrainedOCR(String filename, Mat& sample, Mat& response);
void saveTrainedOCR(String filename, Mat& sample, Mat& response);
int getNumberOCR(Mat img, Ptr<KNearest> knn);


#endif