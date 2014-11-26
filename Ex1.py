
# maplot
# Roy Haggerty
# 2014


def get_data():
    """ Returns tuple of data"""
    data= {\
            'McKenzie':                 (-123.1043, 44.1256,    1,  3307033881.96,-122.287768,  44.14907, 1, 1), \
            'Middle Fork Willamette':   (-122.9073, 43.9998,    2,  3482874058.62,-122.39528,	43.757159, 19, 10),\
            'Upper Yamhill':            (-123.1445, 45.2257,    3,  1340602668.23, -123.440166,	45.095052, 21, 11),\
            'Pudding':                  (-122.7162, 45.2976,    4,  2268590002.85,-122.606776,	45.0444, 3, 2),\
            'Clackamas':                (-122.6077, 45.3719,    5,  2434914144.62,-122.088399,	45.11371, 5, 3),\
            'Long Tom':                 (-123.2569, 44.3807,    6,  1050268949.3,-123.309363,	44.088905, 7, 4),\
            'Marys':                    (-123.2615, 44.5564,    7,  778831948.728,-123.429468,	44.504221, 9, 5),\
            'North Santiam':            (-123.1432, 44.7501,    8,  1976850713.48,-122.230379,	44.715461, 11, 6),\
            'South Santiam':            (-123.007,  44.6855,    9,  2694079717.91,-122.522354,	44.517834, 13, 7),\
            'Tualatin':                 (-122.6501, 45.3377,    10, 1829685666.99,-123.052358,	45.538177, 15, 8),\
            'Coast Fork Willamette':    (-123.0082, 44.0208,    11, 1691632167.43,-122.901411,	43.719156, 17, 9),\
            'Willamette':               (-122.7651, 45.6537,    12 , 29728000000., -122.7651,    45.6537, 2, 1)\
            }
    scenarios = {\
            'Reference':                '_Ref_Run0',\
            'HighClim':                 '_HighClim_Run0',\
            'LowClim':                  '_LowClim_Run0',\
            'HighPop':                  '_HighPop_Run0',\
            'UrbExpand':                '_UrbExpand_Run0',\
            'FireSuppress':             '_FireSuppress_Run0'\
            }

    return data, scenarios

def getfilenames(data_path, searchword):
    import glob
    files = glob.glob(data_path + '/*.csv')
    filenamelist = []
    fileswopath = [eachfile.partition(data_path)[2] for eachfile in files]    
    for filename in fileswopath:
        if filename.startswith(searchword): filenamelist.append(data_path+filename)
    return filenamelist
    
def ct(water_yr_array):
    """
    Calculate center of timing for each water year in the water_yr_array
    Return CT for each year (vector)
    water_yr_array = array size 365 by water years containing values
    """
    CT = np.zeros_like(range(0, water_yr_array.shape[0]))
    m0 = np.zeros_like(range(0, water_yr_array.shape[0]))
    m1 = np.zeros_like(range(0, water_yr_array.shape[0]))
    m0 = [np.trapz(water_yr_array[i,:], x=None, dx=1.0, axis=-1) for i in range(89)]
    m1 = [np.trapz(np.multiply(water_yr_array[i,:],range(365)), x=None, dx=1.0, axis=-1) for i in range(89)]
    CT = np.divide(m1,m0) + cst.day_of_year_oct1
    return CT

def get_metadata():
    """Add metadata to plot
    """
    import time as timetool, os.path
    textstr = 'Willamette Water 2100' + \
              '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
              '\n' + '  File: ' + file_nm +\
              '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))        
    return textstr
    
def write_tinyfigs(datalist,figsize,mind,maxd,redblue, num_yrs):
    """Write tiny figs to be plotted on map
    """
    from matplotlib import pyplot as plt
    
    for i in range(len(datalist)):
        plt.figure(figsize = figsize[i])
        plt.axis('off')
        plt.ylim( (mind,maxd) )
        plt.fill_between(range(num_yrs),0.,datalist[i],where=datalist[i]>=0., facecolor=redblue[0],lw=0,alpha=0.95) 
        plt.fill_between(range(num_yrs),0.,datalist[i],where=datalist[i]<=0., facecolor=redblue[1],lw=0,alpha=0.95) 
        plt.savefig('tinyfig'+str(i)+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
        plt.close()

    return


def write_legend(data,figsize,mind,maxd,redblue, num_yrs,ylabel,xlabel):
    """Write tiny legend to be plotted on map
    """
    from matplotlib import pyplot as plt
    
    figleg = plt.figure(figsize=figsize)
    axleg = Subplot(figleg,111)
    figleg.add_subplot(axleg)
    axleg.axis['top'].set_visible(False)
    axleg.axis['bottom'].set_visible(False)
    axleg.axis['right'].set_visible(False)
    yloc = plt.MaxNLocator(5)
    axleg.yaxis.set_major_locator(yloc)
    plt.ylim( (mind,maxd) )
    plt.fill_between(range(num_yrs),0.,data,where=data>=0., facecolor=redblue[0],lw=0,alpha = 0.95) 
    plt.fill_between(range(num_yrs),0.,data,where=data<=0., facecolor=redblue[1],lw=0,alpha = 0.95) 
    font = {'size':'6'}           
    mpl.rc('font', **font)
    plt.ylabel(ylabel, fontsize=6)
    axleg.text(-30., mind*1.5, xlabel, fontsize=6,
            verticalalignment='top')
    plt.savefig('tinyfig'+'12'+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
    plt.close()
    mpl.rcdefaults()

    return
    
    
def write_map(title, lons, lats, file_graphics, textstr, shp, graphs=range(13)):
    """Write the map
    """
    from matplotlib import pyplot as plt
    
    fig = plt.figure(figsize=(6,8))
    ax2 = fig.add_axes()
    plt.axes(frameon=False)
    
    WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
    im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
    WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
    WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
    
    plt.title(title)
    
    x,y=WBmap(lons,lats)
    
    plt.text(0., 0., textstr, fontsize=3,verticalalignment='top')        
    for i in graphs:
        marker = np.array(Image.open('tinyfig'+str(i)+'.png'))
        im = OffsetImage(marker, zoom=1)
        ab = AnnotationBbox(im, (x[i],y[i]), xycoords='data', frameon=False, box_alignment=(xctr, yctr))
        WBmap._check_ax().add_artist(ab)
#        plt.show()
    plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
    plt.close()       

    return

###############################################################################
###############################################################################
###############################################################################

import matplotlib as mpl
from mpl_toolkits.axes_grid.axislines import Subplot
from matplotlib import pyplot as plt
from mpl_toolkits import basemap
from matrix_from_xls import matrix_from_xls as mfx
import constants as cst
import numpy as np
import datetime
from Rectangle import np_rec_calc as nrc
from compare import compare_rows
import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from movingaverage import movingaverage, binomial_window

lat_bounds = 43.31342817420548, 45.84870876153576
long_bounds = -121.401130054521,-124.151784119791

subbasin_data, scenarios = get_data()

shp = 'C:\\code\\maplot\\shpf\\Sub_Area_gc'
png_path = 'C:\\code\\maplot pngs\\'
data_path = 'C:\\code\\maplot data\\'

subbasin_data_list = [subbasin_data[key] for key in subbasin_data]
subbasin_data_list = sorted(subbasin_data_list,key=lambda x: x[2])  # order list by column number
subbasin_data_lons = [subbasin_data_list[i][4] for i in range(len(subbasin_data_list))]
subbasin_data_lats = [subbasin_data_list[i][5] for i in range(len(subbasin_data_list))]
subbasin_data_order = [subbasin_data_list[i][2] for i in range(len(subbasin_data_list))]
subbasin_data_area = [subbasin_data_list[i][3] for i in range(len(subbasin_data_list))]
subbasin_data_climate_col = [subbasin_data_list[i][6] for i in range(len(subbasin_data_list))]
subbasin_data_snow_col = [subbasin_data_list[i][7] for i in range(len(subbasin_data_list))]

lons = subbasin_data_lons
lons[11]=subbasin_data_lons[11]+0.2
lons.append(-123.8)
lats = subbasin_data_lats
lats.append(43.9)

figsize=[(0.6,0.6) for i in range(11)]
figsize.append((1.1,0.6))
figsize_leg = (0.6,0.6)

#plots_to_plot = range(4,5)
plots_to_plot = [7]
print 'Plots to be plotted are:', '\t', plots_to_plot
for plot_num in plots_to_plot:
    
    
############  Specific Discharge ############    
    if plot_num == 0: 
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        plt.title("Specific Discharge")
        file_nm = data_path + 'Discharge_(Subbasins)_Ref_Run0.csv'
        data1=[mfx(file_nm,column=subbasin_data_order[i],skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data1_spQ=[np.mean(data1[i])/subbasin_data_area[i]*cst.seconds_in_yr*100. for i in range(12)]
        summer_Q = [nrc(data1[i],[1,260],[88,350]) for i in range(12)]
        
        import heapq
        data1_2nd_lgst = heapq.nlargest(2, summer_Q)[1]  #find second-largest number
        data1_size = np.clip(200.*np.array(summer_Q)/data1_2nd_lgst,30.,20000.)
        
        colord = np.array(data1_spQ)
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],128)
        WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'spQ.png'     
        plt.text(0., 0, get_metadata(), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       
        
############  Summer Hydrologic Drought ############    
    elif plot_num == 1:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Summer Hydrologic Drought")
        
        file_nm = data_path + 'Discharge_(Subbasins)_Ref_Run0.csv'

        data1=[mfx(file_nm, column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd1 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        Q10 = [np.percentile(data_avg[i][0:10,:], 10.,axis=0) for i in range(12)]
        data_hd_binary = [compare_rows(data_avg[i],Q10[i]) for i in range(12)]  #1's are drought
        
        diff_drought_days = [
                       nrc(data_hd_binary[i],[69,260],[88,350], oper='sum') \
                    -  nrc(data_hd_binary[i],[0, 260],[19,350], oper='sum') \
                    for i in range(12)]  #+ve numbers are increasing drought
       
        colord = np.array(diff_drought_days)
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['blue','white','red'],128)
        WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'drought_days.png'        
        plt.text(0., 0, get_metadata(), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       



############  Precipitation ############    
    elif plot_num == 2:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Annual Precipitation")
        
        file_nm = data_path + 'Climate_(Subbasin)_Ref_Run0.csv'
        data1=[mfx(file_nm, column=subbasin_data_climate_col[i], skip=cst.day_of_year_oct1) for i in range(11)]
        file_nmWB = data_path + 'Climate_Ref_Run0.csv'
        data1.append(mfx(file_nmWB, column=subbasin_data_climate_col[11], skip=cst.day_of_year_oct1))
        data_hd1 = data1
        
        diff_ann_precip = [
                    + nrc(data_hd1[i],[0,0],[19,364], oper='avg') \
                    - nrc(data_hd1[i],[69, 0],[88,364], oper='avg') \
                    for i in range(12)]  # +ve numbers are decreasing precip
        print nrc(data_hd1[0],[0,0],[19,364], oper='avg')
        print nrc(data_hd1[0],[69, 0],[88,364], oper='avg')
        print diff_ann_precip
       
        colord = np.array(diff_ann_precip)
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['blue','white'],128)
        WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'diff_ann_precip.png'        
        plt.text(0., 0, get_metadata(), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       



############  Winter Temperature ############    
    elif plot_num == 3:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Winter (Nov 1 - Mar 31) Temp")
        
        file_nm = data_path + 'Climate_(Subbasin)_Ref_Run0.csv'
        data1=[mfx(file_nm, column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1) for i in range(11)]
        file_nmWB = data_path + 'Climate_Ref_Run0.csv'
        data1.append(mfx(file_nmWB, column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd1 = data1
        
        diff_winter_temp = [
                      nrc(data_hd1[i],[69,31],[88,182], oper='avg') \
                    - nrc(data_hd1[i],[0, 31],[19,182], oper='avg') \
                    for i in range(12)]  #+ve numbers are increasing temp
        print 'early cent', '\t',nrc(data_hd1[i],[69,31],[88,182], oper='avg')
        print 'late cent', '\t',nrc(data_hd1[i],[0, 31],[19,182], oper='avg')
        print np.array(diff_winter_temp)
       
        colord = np.array(diff_winter_temp)
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','red'],128)
        WBmap.scatter(x, y, marker='o',  s=200., lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'diff_winter_Temp.png'        
        plt.text(0., 0, get_metadata(), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       




############  Summer Hydrologic Drought w mini figs ############    
    elif plot_num == 4:
        file_nm = data_path + 'Discharge_(Subbasins)_Ref_Run0.csv'
       
        plt.close()
        data1=[mfx(file_nm, column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd1 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        Q10 = [np.percentile(data_avg[i][0:10,:], 10.,axis=0) for i in range(12)]
        data_hd_binary = [compare_rows(data_avg[i],Q10[i]) for i in range(12)]  #1's are drought
        
        summer_dr_d = [np.sum(data_hd_binary[i][:,260:351],1) for i in range(12)]
        baseline = [np.mean(summer_dr_d[i][:30]) for i in range(12)]
        
        window = binomial_window(15)
        summer_dr_d_smthd = [np.subtract(movingaverage(summer_dr_d[i],window), baseline[i]) for i in range(12)]
        maxd = np.max(np.array([np.max(summer_dr_d_smthd[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(summer_dr_d_smthd[i]) for i in range(12)]))
        xctr = 0.5
        yctr = 0.5

        redblue = ['red','blue']
        num_yrs = len(summer_dr_d_smthd[0])
        write_tinyfigs(summer_dr_d_smthd,figsize,mind,maxd,redblue, num_yrs)
        
        ylabel = r'$\Delta \, Drought\,$ [days]'
        xlabel = 'Red = Drier'
        write_legend(summer_dr_d_smthd[0],figsize_leg,mind,maxd,redblue,num_yrs,ylabel,xlabel)
               
        title = "Change in Summer Hydrologic Drought"
        file_graphics = 'change_in_drought_days_wGrphs.png'

        write_map(title, lons, lats, file_graphics, get_metadata(), shp)




############  Winter Temperature w mini figs ############    
    elif plot_num == 5:
        file_nm = data_path + 'Climate_(Subbasin)_Ref_Run0.csv'
        file_nmWB = data_path + 'Climate_Ref_Run0.csv'
       
        plt.close()
        data1=[mfx(file_nm, column=subbasin_data_order[i]+1, skip=cst.day_of_year_oct1) for i in range(11)]
        data1.append(mfx(file_nmWB, column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd1 = data1
        data_winter = [data_hd1[i][:,31:182] for i in range(12)]
        winter_tmps = [np.mean(data_winter[i],1) for i in range(12)]  # avg over winter each year for ea subbasin
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_order[i]+1, skip=cst.day_of_year_oct1)
                   for i in range(11)]
        data1.append(mfx(file_nmWB.replace('_Ref_','_HighClim_'), column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_order[i]+1, skip=cst.day_of_year_oct1)
                   for i in range(11)]
        data1.append(mfx(file_nmWB.replace('_Ref_','_LowClim_'), column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        baseline = [nrc(data_avg[i],[0, 10],[29,182]) for i in range(12)]  
                
        window = binomial_window(15)
        winter_temps_smthd = [np.subtract(movingaverage(winter_tmps[i],window), baseline[i])[8:83] for i in range(12)]
        maxd = np.max(np.array([np.max(winter_temps_smthd[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(winter_temps_smthd[i]) for i in range(12)]))
        xctr = 0.5
        yctr = 0.75

        redblue = ['red','blue']
        num_yrs = len(winter_temps_smthd[0])
        write_tinyfigs(winter_temps_smthd,figsize,mind,maxd,redblue, num_yrs)
        
        ylabel = r'$\Delta \, Temp\,$ [$^{\circ}\mathrm{C}$]'
        xlabel = 'Red = Warmer'
        write_legend(winter_temps_smthd[0],figsize_leg,mind,maxd,redblue,num_yrs,ylabel,xlabel)
        
        title = "Change in Winter Temperatures (Nov - Mar)"
        file_graphics = 'change_in_winter_temp_wGrphs.png'

        write_map(title, lons, lats, file_graphics, get_metadata(), shp)




############  Econ w mini figs ############    
    elif plot_num == 6:
        plt.close()
        
        econ_files = getfilenames(data_path,'subbasin')
        econ_fileswopath = [eachfile.partition(data_path)[2] for eachfile in econ_files]
        for file_nm in econ_files:
#            file_nm=data_path+'subbasin_tot_ac_of_developed_land_by_SUB_AREA_EarlyReFill_Run0.csv'
            file_nmWB = file_nm     
            title = file_nm.partition(data_path)[2][:-4]
            png_file_nm = title+'.png'
            data_v = np.array(np.genfromtxt(file_nm, delimiter=',',skip_header=1)) # Read csv file
            data1 = [data_v[2:,subbasin_data_order[i]+1] for i in range(11)]
            data1.append(data_v[2:,1])
            data1 = [np.subtract(data1[i],data1[i][0]) for i in range(11)]
            maxd = np.max(np.array([np.max(data1[i]) for i in range(11)]))
            mind = np.min(np.array([np.min(data1[i]) for i in range(11)]))
            if maxd >= abs(mind):
                xctr = 0.75
                yctr = 0.5
            else:
                xctr = 0.75
                yctr = 0.7
                
            redblue = ['red','blue']
            num_yrs = len(data1[0])
            write_tinyfigs(data1,figsize,mind,maxd,redblue, num_yrs)
            
            ylabel = r'$\Delta \, value\,$'
            xlabel = ' '
            write_legend(data1[4],figsize_leg,mind,maxd,redblue,num_yrs,ylabel,xlabel)
            
            file_graphics = png_file_nm        
    
            graphs = range(11)
            graphs.append(12)
            write_map(title, lons, lats, file_graphics, get_metadata(), shp, graphs=graphs)
            
#            assert False
            
            
            
            
            
############  Econ w mini figs normalized by land area ############    
    elif plot_num == 7:
        plt.close()
        run_names = [\
        ('subbasin_tot_LR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_LR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_LR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv'),\
        ('subbasin_tot_SR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv')\
        ]
        
        for key in scenarios:
            
            for files in run_names:
                files_scen = (files[0].replace(scenarios['Reference'],scenarios[key]),files[1].replace(scenarios['Reference'],scenarios[key]))
                print files_scen
                title = files_scen[0][:-4]
                file_nm_num = data_path + files_scen[0]
                file_nm_denom = data_path + files_scen[1]
                file_nmWB = file_nm_num     
                png_file_nm = title+'_divided_by_area'+'.png'
                data_v_num = np.array(np.genfromtxt(file_nm_num, delimiter=',',skip_header=1)) # Read csv file
                data_v_denom = np.array(np.genfromtxt(file_nm_denom, delimiter=',',skip_header=1)) # Read csv file
                data1_num = [data_v_num[2:,subbasin_data_order[i]+1] for i in range(11)]
                data1_denom = [data_v_denom[2:,subbasin_data_order[i]+1] for i in range(11)]
                data1_num.append(data_v[2:,1])
                data1_denom.append(data_v[2:,1])
                data1 = [np.divide(data1_num[i],data1_denom[i]) for i in range(11)]
                data1 = [np.subtract(data1[i],data1[i][0]) for i in range(11)]
                maxd = np.max(np.array([np.max(data1[i]) for i in range(11)]))
                mind = np.min(np.array([np.min(data1[i]) for i in range(11)]))
                if maxd >= abs(mind):
                    xctr = 0.75
                    yctr = 0.5
                else:
                    xctr = 0.75
                    yctr = 0.7
                    
                redblue = ['red','blue']
                num_yrs = len(data1[0])
                write_tinyfigs(data1,figsize,mind,maxd,redblue, num_yrs)
                
                ylabel = r'$\Delta \, Value\,$' +r'[\$/ac]'
                xlabel = ' '
                write_legend(data1[4],figsize_leg,mind,maxd,redblue,num_yrs,ylabel,xlabel)
                
                file_graphics = png_file_nm        
        
                graphs = range(11)
                graphs.append(12)
                write_map(title, lons, lats, file_graphics, get_metadata(), shp, graphs=graphs)
                
#                assert False
            
            
            
            
            ############  Center of Timing w mini figs ############    
    elif plot_num == 8:
        file_nm = data_path + 'Discharge_(Subbasins)_Ref_Run0.csv'
       
        plt.close()
        data1=[mfx(file_nm, column=subbasin_data_order[i], skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd1 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_order[i], 
                   skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_order[i], 
                   skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        ctList = [np.array(ct(data_avg[i])) for i in range(12)]
        ctdata_hd1 = [np.array(ct(data_hd1[i])) for i in range(12)]
        
        baseline = [np.mean(ctList[i][:30]) for i in range(12)]
        
        window = binomial_window(15)
        delta_discharge_timing = [-1.*np.subtract(movingaverage(ctdata_hd1[i],window), baseline[i]) for i in range(12)]
        maxd = np.max(np.array([np.max(delta_discharge_timing[i][8:83]) for i in range(12)]))
        mind = np.min(np.array([np.min(delta_discharge_timing[i][8:83]) for i in range(12)]))
        print 'Max timing advance = ','\t',maxd
        print 'Min timing advance = ','\t',mind
        delta_discharge_timing = np.array([delta_discharge_timing[i][8:83] for i in range(12)])

        redblue = ['red','blue']
        num_yrs = len(delta_discharge_timing[0])
        write_tinyfigs(delta_discharge_timing,figsize,mind,maxd,redblue, num_yrs)
        
        ylabel = r'$\Delta \, CT\,$ [days]'
        xlabel = 'Red = Earlier'
        write_legend(delta_discharge_timing[0],figsize_leg,mind,maxd,redblue,num_yrs,ylabel,xlabel)
            
        title = "Change in Timing of Discharge (CT)"
        file_graphics = 'change_in_discharge_timing_wGrphs.png'        

        write_map(title, lons, lats, file_graphics, get_metadata(), shp)




############  Max SWE w mini figs ############    
    elif plot_num == 9:
        file_nm = data_path + 'Snow_(Subbasin)_Ref_Run0.csv'
        file_nmWB = data_path + 'Snow_(mm)_Ref_Run0.csv'
       
        plt.close()
        data1=[mfx(file_nm, column=subbasin_data_snow_col[i], skip=cst.day_of_year_oct1) for i in range(11)]
        data1.append(mfx(file_nmWB, column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
        SWE1 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
        
        data1=[mfx(file_nm.replace('_Ref_','_HighClim_'), column=subbasin_data_snow_col[i], skip=cst.day_of_year_oct1)
                   for i in range(11)]
        data1.append(mfx(file_nmWB.replace('_Ref_','_HighClim_'), column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
        SWE2 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
        
        data1=[mfx(file_nm.replace('_Ref_','_LowClim_'), column=subbasin_data_snow_col[i], skip=cst.day_of_year_oct1)
                   for i in range(11)]
        data1.append(mfx(file_nmWB.replace('_Ref_','_LowClim_'), column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
        SWE3 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
        
        SWE_avg = [(SWE1[i]+SWE2[i]+SWE3[i])/3. for i in range(12)]
        baseline = [np.mean(SWE_avg[i][0:10]) for i in range(12)]  #1's are drought
                
        window = binomial_window(15)
        SWE_smthd = [np.subtract(movingaverage(SWE1[i],window), baseline[i]) for i in range(12)]
        maxd = np.max(np.array([np.max(SWE_smthd[i][8:83]) for i in range(12)]))
        mind = np.min(np.array([np.min(SWE_smthd[i][8:83]) for i in range(12)]))
        SWE_smthd = [SWE_smthd[i][8:83] for i in range(12)]
        xctr = 0.5
        yctr = 0.75
        
        redblue = ['blue','red']
        num_yrs = len(SWE_smthd[0])
        write_tinyfigs(SWE_smthd,figsize,mind,maxd,redblue, num_yrs)
        
        ylabel = r'$\Delta \, SWE\,$ [cm]'
        xlabel = 'Red = Less SWE'
        write_legend(SWE_smthd[0],figsize_leg,mind,maxd,redblue,num_yrs,ylabel,xlabel)
        
        title = "Change in Basin-Averaged Max SWE"
        file_graphics = 'change_in_max_SWE_wGrphs.png'        

        write_map(title, lons, lats, file_graphics, get_metadata(), shp)
        
