
# First try at plotting on an image of the WB
# Roy Haggerty

import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits import basemap
from mpl_toolkits.basemap import Basemap
from matrix_from_xls import matrix_from_xls as mfx
import constants as cst
import numpy as np

lat_bounds = 43.31342817420548, 45.84870876153576
long_bounds = -121.401130054521,-124.151784119791

ax2 = plt.subplot(111)
ax2.set_title("Specific Discharge of Willamette & Tributaries")

WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
            urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
im = plt.imread('C:\\code\\maplot\\ElevationMap_Willamette.png')
WBmap.imshow(im, origin='upper') #interpolation='lanczos', 

subbasin_pour_points= {\
            'McKenzie':                 (-123.1043, 44.1256,    1,  3307033881.96),\
            'Middle Fork Willamette':   (-122.9073, 43.9998,    2,  3482874058.62),\
            'Upper Yamhill':            (-123.1445, 45.2257,    3,  1340602668.23),\
            'Pudding':                  (-122.7162, 45.2976,    4,  2268590002.85),\
            'Clackamas':                (-122.6077, 45.3719,    5,  2434914144.62),\
            'Long Tom':                 (-123.2569, 44.3807,    6,  1050268949.3),\
            'Marys':                    (-123.2615, 44.5564,    7,  778831948.728),\
            'North Santiam':            (-123.1432, 44.7501,    8,  1976850713.48+2694079717.91),\
            'South Santiam':            (-123.007,  44.6855,    9,  2694079717.91),\
            'Tualatin':                 (-122.6501, 45.3377,    10, 1829685666.99),\
            'Coast Fork Willamette':    (-123.0082, 44.0208,    11, 1691632167.43),\
            'Willamette':               (-122.7651, 45.6537,    12 , 29728000000.)\
            }

shp = 'C:\\Users\\haggertr\\Desktop\\Documents\\work - OSU\\research\\WW2100\\Research\\shapefiles\\Sub_Area_gc2'
WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )

subbasin_pour_points_coords = [subbasin_pour_points[key] for key in subbasin_pour_points]
subbasin_pour_points_lons = [subbasin_pour_points_coords[i][0] for i in range(len(subbasin_pour_points_coords))]
subbasin_pour_points_lats = [subbasin_pour_points_coords[i][1] for i in range(len(subbasin_pour_points_coords))]
subbasin_pour_points_order = [subbasin_pour_points_coords[i][2] for i in range(len(subbasin_pour_points_coords))]
subbasin_pour_points_area = [subbasin_pour_points_coords[i][3] for i in range(len(subbasin_pour_points_coords))]

data1=[mfx('Discharge_(Subbasins)_Ref_Run0.csv',column=subbasin_pour_points_order[i],skip=cst.day_of_year_oct1) for i in range(12)]
data1_spQ=[np.mean(data1[i])/subbasin_pour_points_area[i]*cst.seconds_in_yr*100. for i in range(12)]
colord = np.array(data1_spQ)

p_lon = -123.0867
p_lat = 44.0519
x,y = WBmap(p_lon,p_lat)
x,y=WBmap(subbasin_pour_points_lons,subbasin_pour_points_lats)
cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],128)

WBmap.scatter(x, y, marker='o',  s=100, lw=0,c=colord,cmap = cmap1)
#plt.show()
file_graphics = 'WB.png'
plt.savefig(file_graphics, format="png", dpi=600)
