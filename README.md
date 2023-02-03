# Disillusionment

12/18/2022: I am currently updating the project to mostly C++ to reduce computation time. Will update README.md when finished. 

This project aims to produce acrylic lens that cast shadow patterns that imitate images. The project is largely based on ["Hiding Images in Plain Sight: The Physics Of Magic Windows"](https://mattferraro.dev/posts/caustics-engineering) by Matt Ferraro and "["Poisson-Based Continuous Surface Generation for Goal-Based Caustics"](http://nishitalab.org/user/egaku/tog14/yue-continuous-caustics-lens.pdf)" by Yue et al.

Only square image inputs are allowed at the moment. The results of this projects are concluded in a report [here](https://github.com/FS-Far-Star/Disillusionment/blob/main/Caustics_project.pdf). 

To use this repo, put the desired image in the image folder. Then change the line name_of_file = 'images/protoss_invert.png' in init.py to match your image's name. Run morph_grid, heightmap, and convert_to_stl in order. If you want to see the simulated result, run simulation.py. To get the theoretical output, set error=False. To simulate the output of a manufactured object, leave error=True. 

The resulting .stl file is an acceptable format for most CNC machine. 

<img src="https://github.com/FS-Far-Star/Disillusionment/blob/main/images/figure1.png" alt="right" width="100" height="100"> <img src="https://github.com/FS-Far-Star/Disillusionment/blob/main/images/figure2.png" width="100" height="100"> <img src="https://github.com/FS-Far-Star/Disillusionment/blob/main/images/figure3.png" width="100" height="100">

### Technical stuff: ###

__init.py:__ Import necessary libraries, specify real-world parameters (width, height, and thickness of persplex piece, projection distance, persplex refractive index, etc.), specify target image and convert it to greyscale. 

__functions.py:__ Python functions defined to make the program more readible. 

__loading.py:__ Read data from excel worksheets so that different parts can be tested separately.

__plotting.py:__ Plots anything from the grid layout to the 3d object. Mainly used for development. 

__morph_grid.py:__ A uniform square grid is generated. Establish one-to-one relation between image pixels and grid cells, i.e. if pixel is bright, the area of its corresponding grid cell should be large. Enforce this relation through iterations and gradient descent until convergence (Sometimes it oscillates with mean = 0, which is Okay). Output x and y coordinates of grid points to two excel worksheets. The result specifies a 2d grid layout. 

__heightmap.py:__ Continue operation on the 2d grid. Using small-angle approximation and refraction laws, calculate the necessary z-coordinate such that light passing through cell(i,j) is refracted to go to the correct "pixel location" on the projection plane. Since changing z-coordinate changes the distance between the incidental surface and the projection plane, iterate a few times to ensure convergence. Output z coordinates of grid points to an excel worksheet. Now a 3d object is specified.

__convert_to_stl.py:__ Import data using loading, pack the grid points into triangles to define the outer surface of the object. This can then be converted into .stl format for manufacturing. 

__simulation.py:__ Import data using loading, assuming parallel incidental light, use refraction laws to calculate the theorectical output (and save it as a PNG image). A random error can be introduce to simulate the actual output of the manufactured object, but does NOT work very well.  
