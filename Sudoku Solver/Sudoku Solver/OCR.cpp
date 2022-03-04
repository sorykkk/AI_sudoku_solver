#include "OCR.h"
#include "Image.h"

void trainOCR(String filename, Mat& sample, Mat& response)
{
	//Procesam imaginea pentru extragerea conturilor
	Mat img_src, img_gra, img_p, img_contours, mat_tmp;

	img_src = imread(filename, IMREAD_UNCHANGED);//load image unchanged

	//verificam sursa de imagine
	if (img_src.empty()) throw String("Image " + filename + " cannot be loaded");

	//arata imaginea originala a train data
	namedWindow("Train Data", WINDOW_AUTOSIZE);

	cout << "input red square number [0-9] or ESC directly from the Train Data window" << endl;
	
	//pre-procesarea imaginea inainte luarii contururilor
	img_p = processInput(img_src);
	img_contours = img_p.clone();

	//gasirea tuturor contururilor
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;

	findContours(img_contours, contours, hierarchy, RETR_CCOMP, CHAIN_APPROX_SIMPLE);

	//iteram prin primul nivel de contur al ierarhiei
	for (int i = 0; i < contours.size(); i = hierarchy[i][0])
	{
		//gasing bounding rectangle
		Rect rect = boundingRect(contours.at(i));

		//omitem dreptunghiurile prea mici in inaltime
		if (rect.height <= train_height_min)
			continue;

		//desenam un dreptunghi rosu pentru a indica data pentru antrenare
		rectangle(img_src, Point(rect.x, rect.y), Point(rect.x + rect.width, rect.y + rect.height), Scalar(0, 0, 255));

		resize(img_p(rect), mat_tmp, Size(matching_size, matching_size), 0, 0, INTER_LINEAR);

		//convertim in float
		mat_tmp.convertTo(img_contours, CV_32FC1);

		//citirea etichetelor corespunzatoare pentru contur de la keyboard
		int key = displayImage("Train Data", img_src);

		//convertirea numarului in integer
		if (key >= '0' && key <= '9')
		{
			//convertim ASCII in valori integeri
			key -= '0';
		}
		//in caz contrar skipuim inputul (numai numere)
		else continue;

		cout << "number " << key << " trained" << endl;

		//pastram eticheta
		response.push_back(key);

		//pastram data
		sample.push_back(img_contours.reshape(1, 1));

		//desenam un dreptunghi verde 
		rectangle(img_src, Point(rect.x, rect.y), Point(rect.x + rect.width, rect.y + rect.height), Scalar(0, 255, 0));
	}

	destroyWindow("Train Data");

	cout << "File trained" << endl;
}

void loadTrainedOCR(String filename, Mat& sample, Mat& response)
{
	Mat mat_tmp;

	//incarcam data din filename
	FileStorage OCR(filename, FileStorage::READ);

	//intoarcem data
	OCR["sample"] >> sample;
	OCR["response"] >> response;
	OCR.release();

	//reshape matricea continua
	mat_tmp = response.reshape(1, response.cols);

	//convertim in data cu semn
	mat_tmp.convertTo(response, CV_32S);

	cout << "Samples and responses loaded from " << filename << endl;

}

void saveTrainedOCR(String filename, Mat& sample, Mat& response)
{
	Mat mat_tmp;

	//reshape matricea pt antrenare
	mat_tmp = response.reshape(1, 1);

	//convertim in float
	mat_tmp.convertTo(response, CV_32F);

	//pastram data in filename
	FileStorage OCR(filename, FileStorage::WRITE);
	OCR << "sample" << sample << "response" << response;
	OCR.release();

	cout << "Sample and responses saved to " << filename << endl;
}

int getNumberOCR(Mat img, Ptr<KNearest> knn)
{
	//copiem inainte sa gasim contururile
	Mat img_contours = img.clone();

	//afisam contururile
	Mat img_color;
	cvtColor(img, img_color, COLOR_GRAY2BGR);

	//gasim contururile 
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;

	//gasirea tuturor contururilor
	findContours(img_contours, contours, hierarchy, RETR_LIST, CHAIN_APPROX_SIMPLE);

	int best_number = 0, best_distance = INT32_MAX;

	//iteram prin primul nivel de contur al hierarchy
	for (auto i : contours)
	{
		Mat img_tmp, img_num;

		//cream vector pentru a lua respunsul si distanta
		vector<float> response, distance;

		//gasim bounding rectangle
		Rect rect = boundingRect(i);

		//procesam doar dreptunghii cu inaltime corespunzatoare marimii numarului
		if (rect.height > matching_size * 0.8 && rect.height <= matching_size * 1.5)
		{
			//facem resize la imagine la forma dreptunghiului
			resize(img(boundingRect(i)), img_tmp, Size(matching_size, matching_size), 0, 0, INTER_LINEAR);
			
			//convertim in float
			img_tmp.convertTo(img_num, CV_32FC1);

			//gasim nearest
			knn->findNearest(img_num.reshape(1, 1), 1, noArray(), response, distance);

			//salvam cel mai bun rezultat sub threshold-erul de distante
			if (distance.at(0) < minimum_matching_dist && distance.at(0) < best_distance)
			{
				best_distance = (int)distance.at(0);
				best_number = (int)response.at(0);
			}

		}
	}

	if (best_number != 0)
		cout << "number solved: " << best_number << " @" << best_distance << endl;

	return best_number;
}