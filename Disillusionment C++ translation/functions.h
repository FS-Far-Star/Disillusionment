#include <iostream>
#include <cstdlib>

using namespace std;
int reset() {
	return 0;
}

int area(float ax, float bx, float cx, float dx, float ay, float by, float cy, float dy) {
	float area1, area2;
	float a1, a2, a3, a4;
	a1 = abs((bx - ax) * (cy - by) - (by - ay) * (cx - bx))/2;	//triangle ABC
	a2 = abs((dx - ax) * (cy - dy) - (dy - ay) * (cx - dx))/2;	//triangle ADC

	a3 = abs((bx - ax) * (dy - by) - (by - ay) * (dx - bx))/2;	//triangle ABD
	a4 = abs((bx - cx) * (dy - by) - (by - cy) * (dx - bx))/2;	//triangle CBD

	area1 = a1 + a2;
	area2 = a3 + a4;

	if (abs(area1 - area2) < 1e-6) {
		return area1;
	}
	else
	{
		cout << "Error: NOT convex" << endl;
	}
}