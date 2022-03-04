#include "Image.h"

int displayImage(const String display_name, Mat img)
{
	Mat display;

	//pastreaza ratia, face resize si afiseaza
	resize(img, display, Size(400, (int)((double)img.rows / img.cols * 400)));
	imshow(display_name, display);

	//asteapta userul sa raspunda
	return waitKey(0);
}

Mat processInput(Mat img)
{
	Mat img_gray, img_adpth;

	//convert in gray
	if (img.channels() == 3 || img.channels() == 4)
		cvtColor(img, img_gray, COLOR_BGR2GRAY);
	else
		img_gray = img.clone();

	//adaptive treshold
	adaptiveThreshold(img_gray, img_adpth, 255, 1, 1, 15, 10);

	return img_adpth;
}

void transformScrabble(Mat img, Mat& img_tr, Rect& big_rect)
{
	//prepocesarea imaginii de intrare
	Mat img_contours = processInput(img);

	//gasirea tuturor contururilor
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;

	findContours(img_contours, contours, hierarchy, RETR_LIST, CHAIN_APPROX_SIMPLE);

	//cel mai mare dreptunghi
	int rect_size_max = 0;
	for (auto i : contours)
	{
		vector<Point> contours_poly;

		//aproximam contururile in poligoane
		approxPolyDP(Mat(i), contours_poly, 4, true);

		//procesam doar poligoanele dreptunghiulare
		if (contours_poly.size() == 4 && isContourConvex(contours_poly))
		{
			int rect_size = contourArea(contours_poly, false);

			//area poligonului
			if (rect_size > rect_size_max)
			{
				//salvam cel mai mare dreptunghi
				rect_size_max = rect_size;
				big_rect = boundingRect(Mat(contours_poly));
			}
		}
	}

	//marimea imaginii de iesire carespunzand potrivirea marimii OCR
	Size img_tr_size;
	img_tr_size.width = case_size * 9;
	img_tr_size.height = case_size * 9;

	//coordinatele grid-ului
	Point2f in_c[4], out_c[4];

	//corespunderea marimii celui mai mare dreptunghi
	in_c[0] = Point2f(big_rect.x, big_rect.y);
	in_c[1] = Point2f(big_rect.x + big_rect.width, big_rect.y);
	in_c[2] = Point2f(big_rect.x + big_rect.width, big_rect.y + big_rect.height);
	in_c[3] = Point2f(big_rect.x, big_rect.y + big_rect.height);

	//corespunderea marimii cu marimea de potrivire a OCR
	out_c[0] = Point2f(0, 0);
	out_c[1] = Point2f(img_tr_size.width, 0);
	out_c[2] = Point2f(img_tr_size.width, img_tr_size.height);
	out_c[3] = Point2f(0, img_tr_size.height);

	//aplicam perspective transform pentru imaginea de input
	warpPerspective(img, img_tr, getPerspectiveTransform(in_c, out_c), img_tr_size);
}

void segmentSudoku(Mat img, Mat& img_num, int x, int y)
{
	int x_offset = max(0, x * case_size - crop_size);
	int y_offset = max(0, y * case_size - crop_size);
	int width = case_size + crop_size;
	int height = case_size + crop_size;

	img(Rect(x_offset, y_offset, width, height)).copyTo(img_num);
}

void drawSudoku(Mat img, Rect rect, int grid[9][9])
{
	//desenarea numerelor care lipsesc
	for (int y = 0; y < 9; ++y)
	{
		for (int x = 0; x < 9; ++x)
		{
			//desenarea numarului
			if (grid[x][y] != 0)
			{
				float sudoku_rect_x_offset = rect.x + (rect.width / 9) * (x + 0.25);
				float sudoku_rect_y_offset = rect.y + (rect.height / 9) * (y + 0.75);
				float font_scale = rect.height * 0.0035 - 0.2;

				//desenam numarul rezolvat
				putText(img, to_string(grid[x][y]), Point2f(sudoku_rect_x_offset, sudoku_rect_y_offset), FONT_HERSHEY_SIMPLEX, font_scale, Scalar(0, 255, 0, 255));
			}
		}
	}
}