
# maplot
# Roy Haggerty
# 2014


def get_data():
    """ Returns tuple of data"""
    data= {\
            'McKenzie':                 (-123.1043, 44.1256,    1,  3307033881.96,-122.287768,  44.14907, 1), \
            'Middle Fork Willamette':   (-122.9073, 43.9998,    2,  3482874058.62,-122.39528,	43.757159, 19),\
            'Upper Yamhill':            (-123.1445, 45.2257,    3,  1340602668.23, -123.440166,	45.095052, 21),\
            'Pudding':                  (-122.7162, 45.2976,    4,  2268590002.85,-122.606776,	45.0444, 3),\
            'Clackamas':                (-122.6077, 45.3719,    5,  2434914144.62,-122.088399,	45.11371, 5),\
            'Long Tom':                 (-123.2569, 44.3807,    6,  1050268949.3,-123.309363,	44.088905, 7),\
            'Marys':                    (-123.2615, 44.5564,    7,  778831948.728,-123.429468,	44.504221, 9),\
            'North Santiam':            (-123.1432, 44.7501,    8,  1976850713.48,-122.230379,	44.715461, 11),\
            'South Santiam':            (-123.007,  44.6855,    9,  2694079717.91,-122.522354,	44.517834, 13),\
            'Tualatin':                 (-122.6501, 45.3377,    10, 1829685666.99,-123.052358,	45.538177, 15),\
            'Coast Fork Willamette':    (-123.0082, 44.0208,    11, 1691632167.43,-122.901411,	43.719156, 17),\
            'Willamette':               (-122.7651, 45.6537,    12 , 29728000000., -122.7651,    45.6537, 2)\
            }

    return data

import matplotlib as mpl
from matplotlib import pyplot as plt
from mpl_toolkits import basemap
from matrix_from_xls import matrix_from_xls as mfx
import constants as cst
import numpy as np
import datetime
import time as timetool, os.path
from Rectangle import np_rec_calc as nrc
from compare import compare_rows
import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from movingaverage import movingaverage, binomial_window

lat_bounds = 43.31342817420548, 45.84870876153576
long_bounds = -121.401130054521,-124.151784119791

subbasin_data = get_data()

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

#plots_to_plot = range(4,5)
plots_to_plot = [0,5]
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
        textstr = 'Willamette Water 2100' + \
                  '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
                  '\n' + '  File: ' + file_nm +\
                  '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))        
        plt.text(0., 0, textstr, fontsize=3,
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
        textstr = 'Willamette Water 2100' + \
                  '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
                  '\n' + '  File: ' + file_nm +\
                  '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))        
        plt.text(0., 0, textstr, fontsize=3,
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
        textstr = 'Willamette Water 2100' + \
                  '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
                  '\n' + '  File: ' + file_nm +\
                  '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))        
        plt.text(0., 0, textstr, fontsize=3,
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
        textstr = 'Willamette Water 2100' + \
                  '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
                  '\n' + '  File: ' + file_nm +\
                  '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))        
        plt.text(0., 0, textstr, fontsize=3,
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
        for i in range(11):
            plt.figure(figsize=(0.6,0.6))
            plt.axis('off')
            plt.ylim( (-20,50) )
            plt.fill_between(range(89),0.,summer_dr_d_smthd[i],where=summer_dr_d_smthd[i]>=0., facecolor='red',lw=0,alpha=0.95)
            plt.fill_between(range(89),0.,summer_dr_d_smthd[i],where=summer_dr_d_smthd[i]<=0., facecolor='blue',lw=0,alpha=0.95)
            plt.savefig('tinyfig'+str(i)+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
            plt.close()
        for i in range(11,12):
            plt.figure(figsize=(1.1,0.6))
            plt.axis('off')
            plt.ylim((-20,50))
            plt.fill_between(range(89),0.,summer_dr_d_smthd[i],where=summer_dr_d_smthd[i]>=0., facecolor='red',lw=0,alpha = 0.95)
            plt.fill_between(range(89),0.,summer_dr_d_smthd[i],where=summer_dr_d_smthd[i]<=0., facecolor='blue',lw=0,alpha = 0.95)
            plt.savefig('tinyfig'+str(i)+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
            plt.close()
        
#        diff_drought_days = [
#                       nrc(data_hd_binary[i],[69,260],[88,350], oper='sum') \
#                    -  nrc(data_hd_binary[i],[0, 260],[19,350], oper='sum') \
#                    for i in range(12)]  #+ve numbers are increasing drought

        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Summer Hydrologic Drought")
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        x[11],y[11]=WBmap(subbasin_data_lons[11]+0.2,subbasin_data_lats[11])
        
        file_graphics = 'change_in_drought_days_wGrphs.png'        
        textstr = 'Willamette Water 2100' + \
                  '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
                  '\n' + '  File: ' + file_nm +\
                  '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))        
        plt.text(0., 0, textstr, fontsize=3,
                verticalalignment='top')        
        # Add the plane marker at the last point.
        for i in range(12):
            marker = np.array(Image.open('tinyfig'+str(i)+'.png'))
            im = OffsetImage(marker, zoom=1)
            ab = AnnotationBbox(im, (x[i],y[i]), xycoords='data', frameon=False)
            WBmap._check_ax().add_artist(ab)
#        plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       




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
        baseline = [nrc(data_avg[i],[0, 31],[29,182]) for i in range(12)]  #1's are drought
                
        window = binomial_window(15)
        winter_temps_smthd = [np.subtract(movingaverage(winter_tmps[i],window), baseline[i]) for i in range(12)]
        for i in range(11):
            plt.figure(figsize=(0.6,0.6))
            plt.axis('off')
            plt.ylim( (-3,7) )
            plt.fill_between(range(89),0.,winter_temps_smthd[i],where=winter_temps_smthd[i]>=0., facecolor='red',lw=0,alpha=0.95) 
            plt.fill_between(range(89),0.,winter_temps_smthd[i],where=winter_temps_smthd[i]<=0., facecolor='blue',lw=0,alpha=0.95) 
            plt.savefig('tinyfig'+str(i)+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
            plt.close()
        for i in range(11,12):
            plt.figure(figsize=(1.1,0.6))
            plt.axis('off')
            plt.ylim((-3,7))
            plt.fill_between(range(89),0.,winter_temps_smthd[i],where=winter_temps_smthd[i]>=0., facecolor='red',lw=0,alpha = 0.95) 
            plt.fill_between(range(89),0.,winter_temps_smthd[i],where=winter_temps_smthd[i]<=0., facecolor='blue',lw=0,alpha = 0.95) 
            plt.savefig('tinyfig'+str(i)+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
            plt.close()
        
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_hi-res.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Winter Temperatures (Nov - Mar)")
        
        x,y=WBmap(subbasin_data_lons,subbasin_data_lats)
        x[11],y[11]=WBmap(subbasin_data_lons[11]+0.2,subbasin_data_lats[11])
        
        file_graphics = 'change_in_winter_temp_wGrphs.png'        
        textstr = 'Willamette Water 2100' + \
                  '\n' + '  Graph generated on ' + str(datetime.date.today()) +\
                  '\n' + '  File: ' + file_nm +\
                  '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))        
        plt.text(0., 0, textstr, fontsize=3,
                verticalalignment='top')        
        # Add the plane marker at the last point.
        for i in range(12):
            marker = np.array(Image.open('tinyfig'+str(i)+'.png'))
            im = OffsetImage(marker, zoom=1)
            ab = AnnotationBbox(im, (x[i],y[i]), xycoords='data', frameon=False)
            WBmap._check_ax().add_artist(ab)
#        plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       

