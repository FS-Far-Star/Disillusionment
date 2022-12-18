#include <iostream>
#include "functions.h"

using namespace std;

int main() {

	// Image import
	int image_size = 10;
	float** brightness_comp = new float* [image_size];
	for (int i = 0; i < image_size; i++) {
		brightness_comp[i] = new float[image_size];
	}
	// !!!!! Need to calculate brightness comp here

	// Real world parameters
	float height = 100;
	float width = 100;
	float thickness = 6;
	float proj_distance = 200;

	// Solving parameters
	int poisson_requirement = 1000;
	float sigma = 1.94;
	int morph_grid_requirement = 600;

	// Physics
	float n1 = 1;        //refractive indice of air
	float eta = 1.49;    //refractive indice of acrylic block

	// size issues
	float spacing = height / image_size;
	int oversize = image_size + 1;

	// Define xv,yv
	float** xv = new float* [oversize];
	float** yv = new float* [oversize];
	for (int i = 0; i < oversize; i++) {
		xv[i] = new float[oversize];
		yv[i] = new float[oversize];
	}

	// Define grad_x, grad_y
	float** grad_x = new float* [oversize];
	float** grad_y = new float* [oversize];
	for (int i = 0; i < oversize; i++) {
		grad_x[i] = new float[oversize];
		grad_y[i] = new float[oversize];
	}

	// Generate Square Mesh (xv and yv)
	for (int i = 0; i < oversize; i++)
	{
		for (int j = 0; j < oversize; j++)
		{
			xv[i][j] = j * spacing;
			yv[i][j] = i * spacing;
		}
	}

	// Define phi, area_grid, loss
	float** phi = new float* [image_size];
	float** area_grid = new float* [image_size];
	float** loss = new float* [image_size];
	for (int i = 0; i < image_size; i++) {
		phi[i] = new float[image_size];
		area_grid[i] = new float[image_size];
		loss[i] = new float[image_size];
	}

	//------------Morph Grid-------------------------------------------------------------------------------------------------------------------------------------
	for (int iteration = 0; iteration < morph_grid_requirement; iteration++) {
		// Reset phi, Update area_grid
		for (int i = 0; i < image_size; i++)
		{
			for (int j = 0; j < image_size; j++)
			{
				phi[i][j] = 1;												   //reset phi
				area_grid[i][j] = area(xv[i][j], xv[i][j + 1], xv[i + 1][j + 1], xv[i + 1][j],
					yv[i][j], yv[i][j + 1], yv[i + 1][j + 1], yv[i + 1][j]);   //update area_grid
			}
		}

		// Calculate loss
		float sum_of_loss = 0;
		for (int i = 0; i < image_size; i++)
		{
			for (int j = 0; j < image_size; j++)
			{
				loss[i][j] = area_grid[i][j] - brightness_comp[i][j];
				sum_of_loss += loss[i][j];
			}
		}
		if (abs(sum_of_loss) > 1e-6) {
			cout << "Loss doesn't sum to zero" << endl;
		}

		// Now iterate to solve Poisson's equation
		for (int solve_poisson = 0; solve_poisson < poisson_requirement; solve_poisson++) {
			for (int i = 0; i < image_size; i++) {
				for (int j = 0; j < image_size; j++) {
					float update;
					// Four corner
					if ((i == 0) && (j == 0)) {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i][j] + phi[i + 1][j] + phi[i][j] + phi[i][j + 1] - loss[i][j] * spacing * spacing);
					}
					else if ((i == image_size) && (j == 0)) {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i - 1][j] + phi[i][j] + phi[i][j] + phi[i][j + 1] - loss[i][j] * spacing * spacing);
					}
					else if ((i == image_size) && (j == image_size)) {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i - 1][j] + phi[i][j] + phi[i][j - 1] + phi[i][j] - loss[i][j] * spacing * spacing);
					}
					else if ((i == image_size) && (j == 0)) {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i - 1][j] + phi[i][j] + phi[i][j] + phi[i][j + 1] - loss[i][j] * spacing * spacing);
					}
					// Four sides
					else if (i == 0) {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i][j] + phi[i + 1][j] + phi[i][j - 1] + phi[i][j + 1] - loss[i][j] * spacing * spacing);
					}
					else if (i == image_size) {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i - 1][j] + phi[i][j] + phi[i][j - 1] + phi[i][j + 1] - loss[i][j] * spacing * spacing);
					}
					else if (j == 0) {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i - 1][j] + phi[i + 1][j] + phi[i][j] + phi[i][j + 1] - loss[i][j] * spacing * spacing);
					}
					else if (j == image_size) {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i - 1][j] + phi[i + 1][j] + phi[i][j - 1] + phi[i][j] - loss[i][j] * spacing * spacing);
					}
					// Center 
					else {
						update = (1 - sigma) * phi[i][j] + sigma / 4 * (phi[i - 1][j] + phi[i + 1][j] + phi[i][j - 1] + phi[i][j + 1] - loss[i][j] * spacing * spacing);
					}
					phi[i][j] = update;
				}
			}
		}

		// Calculate grad_x, grad_y
		for (int i = 0; i < oversize; i++) {
			for (int j = 0; j < oversize; j++) {
				// corners
				if (((j == 0) || (j == oversize)) && ((i == 0) || (i == oversize))) {
					grad_x[i][j] = 0;
					grad_y[i][j] = 0;
				}
				// sides
				else if (i == 0) {
					grad_x[i][j] = (phi[i][j] - phi[i][j - 1]) / spacing;
					grad_y[i][j] = 0;
				}
				else if (i == oversize) {
					grad_x[i][j] = (phi[i - 1][j] - phi[i - 1][j - 1]) / spacing;
					grad_y[i][j] = 0;
				}
				else if (j == 0) {
					grad_x[i][j] = 0;
					grad_y[i][j] = (phi[i][j] - phi[i - 1][j]) / spacing;
				}
				else if (j == oversize) {
					grad_x[i][j] = 0;
					grad_y[i][j] = (phi[i][j - 1] - phi[i - 1][j - 1]) / spacing;
				}
				// center
				else {
					grad_x[i][j] = (phi[i][j] - phi[i][j - 1]) / spacing;
					grad_y[i][j] = (phi[i][j] - phi[i - 1][j]) / spacing;
				}
			}
		}

		// find step size
		float step_size = 1e6;
		float stepx, stepy;
		for (int i = 0; i < oversize; i++) {
			for (int j = 0; j < oversize; j++) {
				// corners
				if (((j == 0) || (j == oversize)) && ((i == 0) || (i == oversize))) {
					step_size = step_size; // No change
				}
				// sides
				else if ((i == 0) || (i == oversize)) {
					if (grad_x[i][j] < 0) {
						stepx = (xv[i][j - 1] - xv[i][j]) / grad_x[i][j];
					}
					if (grad_x[i][j] > 0) {
						stepx = (xv[i][j + 1] - xv[i][j]) / grad_x[i][j];
					}
					step_size = min(step_size, stepx);
				}
				else if ((j == 0) || (j == oversize)) {
					if (grad_y[i][j] < 0) {
						stepy = (yv[i - 1][j] - yv[i][j]) / grad_y[i][j];
					}
					if (grad_y[i][j] > 0) {
						stepy = (yv[i + 1][j] - yv[i][j]) / grad_y[i][j];
					}
					step_size = min(step_size, stepy);
				}
				// center
				else {
					if (grad_x[i][j] < 0) {
						stepx = (xv[i][j - 1] - xv[i][j]) / grad_x[i][j];
					}
					if (grad_x[i][j] > 0) {
						stepx = (xv[i][j + 1] - xv[i][j]) / grad_x[i][j];
					}
					step_size = min(step_size, stepx);
					if (grad_y[i][j] < 0) {
						stepy = (yv[i - 1][j] - yv[i][j]) / grad_y[i][j];
					}
					if (grad_y[i][j] > 0) {
						stepy = (yv[i + 1][j] - yv[i][j]) / grad_y[i][j];
					}
					step_size = min(step_size, stepy);
				}
			}
		}

		// Morph Grid

	}
	
	//------------End of Morphing--------------------------------------------------------------------------------------------------------------------------------

	//print array
	for (int i = 0; i < image_size; i++)
		for (int j = 0; j < image_size; j++)
			// Prints ' ' if j != n-1 else prints '\n'         
			cout << area_grid[i][j] << " \n"[j == image_size - 1];


	// Clean up
	for (int i = 0; i < oversize; i++)
	{
		delete[] xv[i];
		delete[] yv[i];
		delete[] grad_x[i];
		delete[] grad_y[i];
	}
	delete[] xv;
	delete[] yv;
	delete[] grad_x;
	delete[] grad_y;

	for (int i = 0; i < image_size; i++)
	{
		delete[] phi[i];
		delete[] area_grid[i];
		delete[] loss[i];
	}
	delete[] phi;
	delete[] area_grid;
	delete[] loss;

	return 0;
}