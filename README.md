# Disillusionment
This project aims to produce acrylic lens that cast shadow patterns that imitate images. The project is largely based on "Hiding Images in Plain Sight: The Physics Of Magic Windows" by Matt Ferraro and "Poisson-Based Continuous Surface Generation for Goal-Based Caustics" by Yue et al. ''

Links as followed: 
https://mattferraro.dev/posts/caustics-engineering

http://nishitalab.org/user/egaku/tog14/yue-continuous-caustics-lens.pdf

Only square image inputs are allowed at the moment. 

To use this repo, put the desired image in the image folder. Then change the line name_of_file = 'images/protoss_invert.png' in init.py to match your image's name. Run morph_grid, heightmap, and convert_to_stl in order. If you want to see the simulated result, run simulation.py. To get the theoretical output, set error=False. To simulate the output of a manufactured object, leave error=True. 

The resulting .stl file is an acceptable format for most CNC machine. 
