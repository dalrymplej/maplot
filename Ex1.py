
# First try at plotting on an image of the WB
# Roy Haggerty

from matplotlib import pyplot as plt
from mpl_toolkits import basemap
from mpl_toolkits.basemap import Basemap
import random

lat_bounds = 43.5, 46.5
long_bounds = -122.25,-124.7

ax2 = plt.subplot(111)
ax2.set_title("Willamette Basin")

WBmap=basemap.Basemap(projection='cyl', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[0], 
            urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[1], ax=ax2)
im = plt.imread('C:\\code\\maplot\\ElevationMap.png')
WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
#m.etopo()

#data_lats = [random.uniform(*lat_bounds) for i in xrange(4)]
#data_lons = [random.uniform(*long_bounds) for i in xrange(4)]
#m.plot(data_lons,data_lats)

p_lon = -123.
p_lat = 45.
x,y = WBmap(p_lon,p_lat)
WBmap.plot(x, y, 'bo', markersize=12)
x1,y1=WBmap(p_lon-.5,p_lat+0.5)
WBmap.plot(x1,y1,'bo', markersize=12)
plt.show()
