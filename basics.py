from init import *

if 'small' in name_of_file:
    testing = True
else:
    testing = False

'''read image'''
img = Image.open(name_of_file).convert('L') #read image, convert to greyscale
np_img = np.array(img)
np_img = np.fliplr(np.rot90(np_img, 2))  #correctly orient photo so that the result is readable

'''Calculate spacing'''
spacing_x = width/np_img.shape[1]   #for the sake of simplicity, the image used is a square,
spacing_y = height/np_img.shape[0]  #so the spacings are equal

'''Plotting Coordinate system'''
x,y = np.linspace(0,width-spacing_x,np_img.shape[0]), np.linspace(0,height-spacing_y,np_img.shape[1])
a,b = np.meshgrid(x,y)

x,y = np.linspace(0,width,np_img.shape[0]+1), np.linspace(0,height,np_img.shape[1]+1)
c,d = np.meshgrid(x,y)

'''Calculate total area'''
A_t = height*width  #total_area

'''Brightness calculation'''
total_brightness = np.sum(np_img)
brightness_comp = np_img/total_brightness