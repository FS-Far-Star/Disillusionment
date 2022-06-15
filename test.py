from shapely.geometry import Polygon

x=[0,0,1,1]
y=[0,1,1,0]
pgon = Polygon(zip(x, y)) # Assuming the OP's x,y coordinates

print(pgon.area)