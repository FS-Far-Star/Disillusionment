# Disillusionment

12/18/2022: I am currently updating the project to mostly C++ to reduce computation time. Will update README.md when finished. 

This project aims to produce acrylic lens that cast shadow patterns that imitate images. The project is largely based on ["Hiding Images in Plain Sight: The Physics Of Magic Windows"](https://mattferraro.dev/posts/caustics-engineering) by Matt Ferraro and "["Poisson-Based Continuous Surface Generation for Goal-Based Caustics"](http://nishitalab.org/user/egaku/tog14/yue-continuous-caustics-lens.pdf)" by Yue et al.

Only square image inputs are allowed at the moment. The results of this projects are concluded in a report [here](https://github.com/FS-Far-Star/Disillusionment/blob/main/Caustics_project.pdf). 

To use this repo, put the desired image in the image folder. Then change the line name_of_file = 'images/protoss_invert.png' in init.py to match your image's name. Run morph_grid, heightmap, and convert_to_stl in order. If you want to see the simulated result, run simulation.py. To get the theoretical output, set error=False. To simulate the output of a manufactured object, leave error=True. 

The resulting .stl file is an acceptable format for most CNC machine. 

<img src="https://github.com/FS-Far-Star/Disillusionment/blob/main/images/figure1.png" alt="right" width="100" height="100"> <img src="https://github.com/FS-Far-Star/Disillusionment/blob/main/images/figure2.png" width="100" height="100"> <img src="https://github.com/FS-Far-Star/Disillusionment/blob/main/images/figure3.png" width="100" height="100">
