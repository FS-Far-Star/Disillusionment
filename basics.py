from init import *

if 'real' in name_of_file:
    testing = False
else:
    testing = True

'''read image'''
img = Image.open(name_of_file).convert('L') #read image, convert to greyscale
np_img = np.array(img)
np_img = np.fliplr(np.rot90(np_img, 2))  #correctly orient photo so that the result is readable

'''Calculate spacing'''
spacing = width/np_img.shape[0]   #for the sake of simplicity, the image used is a square, so the spacings are equal

'''Plotting Coordinate system'''
x,y = np.linspace(0,width-spacing,np_img.shape[0]), np.linspace(0,height-spacing,np_img.shape[1])
a,b = np.meshgrid(x,y)

'''Calculate total area'''
A_t = height*width  #total_area

'''Brightness calculation'''
total_brightness = np.sum(np_img)
brightness_comp = np_img/total_brightness