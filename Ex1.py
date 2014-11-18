
# First try at plotting on an image of the WB
# Roy Haggerty


def get_data():
    """ Returns tuple of data"""
    data= {\
            'McKenzie':                 (-123.1043, 44.1256,    1,  3307033881.96,-122.287768,  44.14907), \
            'Middle Fork Willamette':   (-122.9073, 43.9998,    2,  3482874058.62,-122.39528,	43.757159),\
            'Upper Yamhill':            (-123.1445, 45.2257,    3,  1340602668.23, -123.440166,	45.095052),\
            'Pudding':                  (-122.7162, 45.2976,    4,  2268590002.85,-122.606776,	45.0444),\
            'Clackamas':                (-122.6077, 45.3719,    5,  2434914144.62,-122.088399,	45.11371),\
            'Long Tom':                 (-123.2569, 44.3807,    6,  1050268949.3,-123.309363,	44.088905),\
            'Marys':                    (-123.2615, 44.5564,    7,  778831948.728,-123.429468,	44.504221),\
            'North Santiam':            (-123.1432, 44.7501,    8,  1976850713.48,-122.230379,	44.715461),\
            'South Santiam':            (-123.007,  44.6855,    9,  2694079717.91,-122.522354,	44.517834),\
            'Tualatin':                 (-122.6501, 45.3377,    10, 1829685666.99,-123.052358,	45.538177),\
            'Coast Fork Willamette':    (-123.0082, 44.0208,    11, 1691632167.43,-122.901411,	43.719156),\
            'Willamette':               (-122.7651, 45.6537,    12 , 29728000000., -122.7651,    45.6537)\
            }

    return data

import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits import basemap
from mpl_toolkits.basemap import Basemap
from matrix_from_xls import matrix_from_xls as mfx
import constants as cst
import numpy as np
import datetime
import time as timetool, os.path
from Rectangle import np_rec_calc as nrc

lat_bounds = 43.31342817420548, 45.84870876153576
long_bounds = -121.401130054521,-124.151784119791

ax2=plt.axes(frameon=False)
ax2.set_title("Specific Discharge")
#ax2.set_size_inches(w,h)

WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
            urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
WBmap.imshow(im, origin='upper') #interpolation='lanczos', 

subbasin_data = get_data()

file_nm = 'Discharge_(Subbasins)_Ref_Run0.csv'
shp = 'C:\\code\\maplot\\shpf\\Sub_Area_gc'
WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )

subbasin_data_list = [subbasin_data[key] for key in subbasin_data]
subbasin_data_list = sorted(subbasin_data_list,key=lambda x: x[2])  # order list by column number
subbasin_data_lons = [subbasin_data_list[i][4] for i in range(len(subbasin_data_list))]
subbasin_data_lats = [subbasin_data_list[i][5] for i in range(len(subbasin_data_list))]
subbasin_data_order = [subbasin_data_list[i][2] for i in range(len(subbasin_data_list))]
subbasin_data_area = [subbasin_data_list[i][3] for i in range(len(subbasin_data_list))]

data1=[mfx(file_nm,column=subbasin_data_order[i],skip=cst.day_of_year_oct1) for i in range(12)]
data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
data1_spQ=[np.mean(data1[i])/subbasin_data_area[i]*cst.seconds_in_yr*100. for i in range(12)]
summer_Q = [nrc(data1[i],[1,260],[90,350]) for i in range(12)]
summer_Q[7] = summer_Q[7] - summer_Q[8] # correct N Santiam for S Santiam contribution

import heapq
data1_2nd_lgst = heapq.nlargest(2, summer_Q)[1]  #find second-largest number
data1_size = np.clip(200.*np.array(summer_Q)/data1_2nd_lgst,0,200.)
print data1_size

colord = np.array(data1_spQ)

x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],128)

WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)

# Metadata for bottom right corner
#    metadata_bottomright = metadata_txt +  '\n' \
#          + 'HJA NSF grant DEB-0832652 and' +  '\n' \
#          + 'Roy Haggerty NSF grant EAR-1417603' + '\n'\
#props = dict(boxstyle='round', facecolor='white', alpha=0.85, lw=0)

textstr = 'Willamette Water 2100' + \
          '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
          '\n' + '  File: ' + file_nm +\
          '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))

ax2.text(0., 0, textstr, fontsize=3,
        verticalalignment='top')


#plt.show()
file_graphics = 'WB.png'
plt.savefig(file_graphics, format="png", dpi=600)
