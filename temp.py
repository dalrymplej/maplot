
# maplot
# Roy Haggerty
# 2014

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib as mpl
from mpl_toolkits.axes_grid.axislines import Subplot
from mpl_toolkits import basemap
from matrix_from_xls import matrix_from_xls as mfx
import constants as cst
import datetime
from Rectangle import np_rec_calc as nrc
from compare import compare_rows
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from movingaverage import movingaverage, binomial_window,movingaverage_2D
import math
#import xlrd
from scipy import stats
import pandas as pd
import imp
from statsmodels.formula.api import ols

def get_EFdata():
    """ Returns tuple of data"""
    EFdata= {
            'Salem':                    (-123.3, 44.941741, 1, 'Willamette_at_Salem_(m3_s)_Ref_Run0.csv', 1), 
            'Hills Creek':              (-122.35, 43.57, 2, 'Hills_Creek_Reservoir_(USACE)_Reservoir_Ref_Run0.csv', 4),
            'Fall Creek':               (-122.7, 44.08, 3, 'Fall_Creek_Reservoir_(USACE)_Reservoir_Ref_Run0.csv', 4),
            'Dexter':                   (-122.6, 43.88, 4, 'Dexter_Reservoir_(USACE_-_re-regulating)_Reservoir_Ref_Run0.csv', 4),
            'Big Cliff':                (-122.4, 44.87, 5, 'Big_Cliff_Reservoir_(USACE_-_re-regulating)_Reservoir_Ref_Run0.csv', 4),
            'Foster':                   (-122.641251, 44.55, 6, 'Foster_Reservoir_(USACE)_Reservoir_Ref_Run0.csv', 4),
            'Blue River':               (-122.279801, 44.27, 7, 'Blue_River_Reservoir_(USACE)_Reservoir_Ref_Run0.csv', 4),
            'Cougar':                   (-122.18, 44.12, 8, 'Cougar_Reservoir_(USACE)_Reservoir_Ref_Run0.csv', 4)
            }
# Lat/long of 8 locations:
    DamLocs= {
            'Salem':                    (-123.038507, 44.941741, 1), 
            'Hills Creek':              (-122.423156, 43.676881, 2),
            'Fall Creek':               (-122.739280, 43.951271, 3),
            'Dexter':                   (-122.787811, 43.913641, 4),
            'Big Cliff':                (-122.266989, 44.732960, 5),
            'Foster':                   (-122.641251, 44.414983, 6),
            'Blue River':               (-122.279801, 44.182290, 7),
            'Cougar':                   (-122.231298, 44.107187, 8)
            }
            
    return EFdata, DamLocs
    
def get_allDamLocs():
    """ Returns tuple of data for all dam locations"""
# Lat/long of 8 locations:
    allDamLocs= {
            'Hills Creek':              (-122.423156, 43.676881, 1),
            'Fall Creek':               (-122.739280, 43.951271, 2),
            'Dexter':                   (-122.787811, 43.913641, 3),
            'Big Cliff':                (-122.266989, 44.732960, 4),
            'Foster':                   (-122.641251, 44.414983, 5),
            'Blue River':               (-122.279801, 44.182290, 6),
            'Cougar':                   (-122.231298, 44.107187, 7),
            'Detroit':                  (-122.250739, 44.721682, 8),
            'Green Peter':              (-122.548650, 44.449654, 9),
            'Lookout Point':            (-122.752465, 43.914625, 10),
            'Dorena':                   (-122.955039, 43.786775, 11),
            'Cottage Grove':            (-123.052858, 43.716259, 12),
            'Fern Ridge':               (-123.301178, 44.120915, 13)
            }
            
    return allDamLocs

def get_gauge_info():
    """return list of lists containing file name & gauge number"""
    gauge_info = [
    ["Willamette_at_Portland_(m3_s)",14211720],
    ["Willamette_at_Salem_(m3_s)",14191000],
    ["Willamette_at_Harrisburg_(m3_s)",14166000],
    ["Johnson_at_Milwaukee_(m3_s)",14211550],
    ["Lookout_(m3_s)",14161500],
    ["Mckenzie_at_Walterville_(m3_s)",14163900],
    ["Mckenzie_Belknap_(m3_s)",14158850],
    ["Mckenzie_Clear_Lake_(m3_s)",14158500]
    ]
    return gauge_info
    
def get_EFrules():
    """ Write rules for each location
    For each location, provide rules.
    Return rules.
    """
    shft = 365 - cst.day_of_year_oct1
    shftB = cst.day_of_year_oct1
                                   ##      rule_type    start_day             end_day              discharge            pct_time_met  weight
    EFrules = {
            'Salem':              (1, (  ['minQ7day', cst.day_of_year_apr1 + shft,  cst.day_of_year_apr30 + shft,  17800.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ7day', cst.day_of_year_may1 + shft,  cst.day_of_year_may31 + shft,  15000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ7day', cst.day_of_year_jun1 + shft,  cst.day_of_year_jun15 + shft,  13000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ7day', cst.day_of_year_jun16 + shft, cst.day_of_year_jun30 + shft,   8000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_apr1 + shft,  cst.day_of_year_apr30 + shft,  14300.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_may1 + shft,  cst.day_of_year_may31 + shft,  12000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_jun1 + shft,  cst.day_of_year_jun15 + shft,  10500.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_jun16 + shft, cst.day_of_year_jun30 + shft,   7000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_jul1 + shft,  cst.day_of_year_jul31 + shft,   6000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_aug1 + shft,  cst.day_of_year_aug15 + shft,   6000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_aug16 + shft, cst.day_of_year_aug31 + shft,   6500.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   7000.*cst.cfs_to_m3,    100.,    1., 'Ref #5'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct31 - shftB,  7000.*cst.cfs_to_m3,    100.,    1., 'Ref #5']
                                         )), 
                                         
            'Hills Creek':        (2, (
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    400.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_jan31 + shft,    400.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_feb1 + shft,  cst.day_of_year_aug31 + shft,    400.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
                                        
            'Fall Creek':         (3, ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    200.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,   200.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    400.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,   400.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_mar31 + shft,     50.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_apr1 + shft,  cst.day_of_year_jun30 + shft,     80.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jul1 + shft,  cst.day_of_year_aug31 + shft,     80.*cst.cfs_to_m3,    95.,     1., 'Ref #1']
                                        )),
                                        
            'Dexter':             (4, ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   1200.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  1200.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   3500.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  3500.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_aug31 + shft,   1200.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
                                        
            'Big Cliff':          (5, ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   1500.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  1500.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   3000.*cst.cfs_to_m3,     5.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  3000.*cst.cfs_to_m3,     5.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_jan31 + shft,   1200.*cst.cfs_to_m3,    98.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_feb1 + shft,  cst.day_of_year_mar15 + shft,   1000.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_mar16 + shft, cst.day_of_year_may31 + shft,   1500.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_mar16 + shft, cst.day_of_year_may31 + shft,   3000.*cst.cfs_to_m3,    25.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jun1 + shft,  cst.day_of_year_jul15 + shft,   1200.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jul16 + shft, cst.day_of_year_aug31 + shft,   1000.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
                                        
            'Foster':             (6, ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   1500.*cst.cfs_to_m3,    75.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  1500.*cst.cfs_to_m3,    75.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,   3000.*cst.cfs_to_m3,     1.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,  3000.*cst.cfs_to_m3,     1.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_jan31 + shft,   1100.*cst.cfs_to_m3,    80.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_feb1 + shft,  cst.day_of_year_mar15 + shft,    800.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_mar1 + shft,  cst.day_of_year_may15 + shft,   1500.*cst.cfs_to_m3,    80.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_mar16 + shft, cst.day_of_year_may15 + shft,   3000.*cst.cfs_to_m3,    30.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_may16 + shft, cst.day_of_year_jun30 + shft,   1100.*cst.cfs_to_m3,    95.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jul1 + shft,  cst.day_of_year_aug31 + shft,    800.*cst.cfs_to_m3,    99.,     1., 'Ref #1']
                                        )),
                                        
            'Blue River':        (7,  ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,     50.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,    50.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_aug31 + shft,     50.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
                                        
            'Cougar':            (8,  ( 
                                         ['minQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    300.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,   300.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_sep1 + shft,  cst.day_of_year_sep30 + shft,    580.*cst.cfs_to_m3,    60.,     1., 'Ref #1'],
                                         ['maxQ',     cst.day_of_year_oct1 - shftB, cst.day_of_year_oct15 - shftB,   580.*cst.cfs_to_m3,    60.,     1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_oct16 - shftB,cst.day_of_year_may31 + shft,    300.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jun1 + shft,  cst.day_of_year_jun30 + shft,    400.*cst.cfs_to_m3,    99.9,    1., 'Ref #1'],
                                         ['minQ',     cst.day_of_year_jul1 + shft,  cst.day_of_year_aug31 + shft,    300.*cst.cfs_to_m3,    99.9,    1., 'Ref #1']
                                        )),
            }
    

    return EFrules

def RuleReliability(data, num_yrs, rules, season='none'):
    """From data (2D numpy array), calculate and return the rule 
    reliability in each year.  
    """
    # Count the number of days that each rule is violated.  Some fraction 
    # (pct_time_met) of violations are allowed.  Beyond that, every violation 
    # counts as 1 * weight.  Violations are summed.
    
    assert num_yrs == np.shape(data)[0]
    shft = 365 - cst.day_of_year_oct1
    start_of_summer = cst.day_of_year_jun1 + shft
#    end_of_summer = cst.day_of_year_sep30 + shft
    num_rules = len(rules)
    violations = np.zeros(num_yrs)
    for j in range(num_rules):
        rule_type = rules[j][0]  # Type of rule
        start_day = rules[j][1]  # Start of the rule
        end_day = rules[j][2]    # End of the rule
        discharge = rules[j][3]  # Discharge for rule
        pct_time_met = rules[j][4] # Percent of time the rule is supposed to be met
        weight = rules[j][5]  # Weights for rules.  This is initially set to 1.
        
        if rule_type == 'minQ':
            num_viols_allowed = math.ceil(float(end_day - start_day + 1) * (100. - pct_time_met)/100.)  # Convert % time met to number of rule violations allowed
            if season == 'none':            
                violations_bool = [data[i,start_day:(end_day+1)] < discharge for i in range(num_yrs)]
            elif season == 'summer':
                if end_day < start_of_summer:
                   violations_bool = np.zeros_like(data, dtype=bool)  # Array of all false
                elif start_day < start_of_summer and end_day >= start_of_summer: 
                    violations_bool = [data[i,start_of_summer:(end_day+1)] < discharge for i in range(num_yrs)]
                elif start_day >= start_of_summer:
                    violations_bool = [data[i,start_day:(end_day+1)] < discharge for i in range(num_yrs)]                    
            elif season == 'not_summer':
                if end_day < start_of_summer:
                   violations_bool = [data[i,start_day:(end_day+1)] < discharge for i in range(num_yrs)]
                elif start_day < start_of_summer and end_day >= start_of_summer: 
                    violations_bool = [data[i,start_day:(start_of_summer+1)] < discharge for i in range(num_yrs)]
                elif start_day >= start_of_summer:
                    violations_bool = np.zeros_like(data, dtype=bool)                    
            violations_prelim = [(np.sum(violations_bool[i]) -num_viols_allowed)*weight for i in range(num_yrs)]
            violations_prelim = np.clip(violations_prelim,0,999999)
            violations += violations_prelim
        elif rule_type == 'maxQ':
            num_viols_allowed = math.ceil(float(end_day - start_day + 1) * (pct_time_met)/100.)  # Convert % time met to number of rule violations allowed
            if season == 'none':            
                violations_bool = [data[i,start_day:(end_day+1)] > discharge for i in range(num_yrs)]
            elif season == 'summer':
                if end_day < start_of_summer:
                   violations_bool = np.zeros_like(data, dtype=bool)
                elif start_day < start_of_summer and end_day >= start_of_summer: 
                    violations_bool = [data[i,start_of_summer:(end_day+1)] > discharge for i in range(num_yrs)]
                elif start_day >= start_of_summer:
                    violations_bool = [data[i,start_day:(end_day+1)] > discharge for i in range(num_yrs)]                    
            elif season == 'not_summer':
                if end_day < start_of_summer:
                    violations_bool = [data[i,start_day:(end_day+1)] > discharge for i in range(num_yrs)]                    
                elif start_day < start_of_summer and end_day >= start_of_summer: 
                    violations_bool = [data[i,start_day:(start_of_summer+1)] > discharge for i in range(num_yrs)]
                elif start_day >= start_of_summer:
                   violations_bool = np.zeros_like(data, dtype=bool)
            violations_prelim = [(np.sum(violations_bool[i]) -num_viols_allowed)*weight for i in range(num_yrs)]
            violations_prelim = np.clip(violations_prelim,0,999999)
            violations += violations_prelim
        elif rule_type == 'minQ7day':
            num_viols_allowed = math.ceil(float(end_day - start_day + 1) * (100. - pct_time_met)/100.)  # Convert % time met to number of rule violations allowed
            data_7dma = movingaverage_2D(data, 7)
            if season == 'none':            
                violations_bool = [data_7dma[i][start_day:(end_day+1)] < discharge for i in range(num_yrs)]
            elif season == 'summer':
                if end_day < start_of_summer:
                   violations_bool = np.zeros_like(data, dtype=bool)
                elif start_day < start_of_summer and end_day >= start_of_summer: 
                    violations_bool = [data_7dma[i][start_of_summer:(end_day+1)] < discharge for i in range(num_yrs)]
                elif start_day >= start_of_summer:
                    violations_bool = [data_7dma[i][start_day:(end_day+1)] < discharge for i in range(num_yrs)]                    
            elif season == 'not_summer':
                if end_day < start_of_summer:
                    violations_bool = [data_7dma[i][start_day:(end_day+1)] < discharge for i in range(num_yrs)]                    
                elif start_day < start_of_summer and end_day >= start_of_summer: 
                    violations_bool = [data_7dma[i][start_day:(start_of_summer+1)] < discharge for i in range(num_yrs)]
                elif start_day >= start_of_summer:
                    violations_bool = np.zeros_like(data, dtype=bool)
            violations_prelim = [(np.sum(violations_bool[i]) -num_viols_allowed)*weight for i in range(num_yrs)]
            violations_prelim = np.clip(violations_prelim,0,999999)
            violations += violations_prelim
        else:
            print '---- Rule requested is not in the code ----'
            assert False
    
    violations = -1*violations
    return violations
    
def get_data():
    """ Returns tuple of data"""
    ##                                  Long (mth)  Lat (mth)  Col     Area       Long (mth)   Lat (mth) Col Col Col
    data= {
            'McKenzie':                 (-123.1043, 44.1256,    1,  3307033881.96,-122.287768,  44.14907, 1, 1, 3), 
            'Middle Fork Willamette':   (-122.9073, 43.9998,    2,  3482874058.62,-122.39528,	43.757159, 19, 10, 21),
            'Upper Yamhill':            (-123.1445, 45.2257,    3,  1340602668.23, -123.440166,	45.095052, 21, 11, 23),
            'Pudding':                  (-122.7162, 45.2976,    4,  2268590002.85,-122.606776,	45.0444, 3, 2, 5),
            'Clackamas':                (-122.6077, 45.3719,    5,  2434914144.62,-122.088399,	45.11371, 5, 3, 7),
            'Long Tom':                 (-123.2569, 44.3807,    6,  1050268949.3,-123.309363,	44.088905, 7, 4, 9),
            'Marys':                    (-123.2615, 44.5564,    7,  778831948.728,-123.429468,	44.504221, 9, 5, 11),
            'North Santiam':            (-123.1432, 44.7501,    8,  1976850713.48,-122.230379,	44.715461, 11, 6, 13),
            'South Santiam':            (-123.007,  44.6855,    9,  2694079717.91,-122.522354,	44.517834, 13, 7, 15),
            'Tualatin':                 (-122.6501, 45.3377,    10, 1829685666.99,-123.052358,	45.538177, 15, 8, 17),
            'Coast Fork Willamette':    (-123.0082, 44.0208,    11, 1691632167.43,-122.901411,	43.719156, 17, 9, 19),
            'Willamette':               (-122.7651, 45.6537,    12 , 29728000000., -122.7651,    45.6537, 2, 1, 1)
            }
            
#    scenarios = {
#            'Reference':                '_Ref_Run0',
#            'HighClim':                 '_HighClim_Run0',
#            'LowClim':                  '_LowClim_Run0',
#            'HighPop':                  '_HighPop_Run0',
#            'UrbExpand':                '_UrbExpand_Run0',
#            'FireSuppress':             '_FireSuppress_Run0',
#            'FullCostUrb':              '_FullCostUrb_Run0',
#            'Extreme':                  '_Extreme_Run0'
    scenarios = {
            'Reference':                '_Ref_Run0',
            'HighClim':                 '_HighClim_Run0',
            'LowClim':                  '_LowClim_Run0',
            'HighPop':                  '_HighPop_Run0',
            'UrbExpand':                '_UrbExpand_Run0',
            'FireSuppress':             '_FireSuppress_Run0',
            'FullCostUrb':              '_FullCostUrb_Run0',
            'Managed':                  '_Managed_Run0',
            'Extreme':                  '_Extreme_Run0'
            }

    scenarios_own = {
            'Reference':                'Reference',
            'HighClim':                 'HighClim',
            'LowClim':                  'Reference',  # !!Change to LowClim once GFDL historical is fixed
            'HighPop':                  'Reference',
            'UrbExpand':                'Reference',
            'FireSuppress':             'Reference',
            'FullCostUrb':              'Reference',
            'Managed':                  'Reference',
            'Extreme':                  'HighClim'
            }
    
    SimulatedHistoric = {
            'Reference':                '_HistoricRef_Run0',
            'HighClim':                 '_HistoricHadGEM_Run0',
            'LowClim':                  '_HistoricRef_Run0'          # !!Change to _HistoricGFDL_Run0 once GFDL historical is fixed
            }
    return data, scenarios, scenarios_own, SimulatedHistoric


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
    num_water_yrs = np.size(water_yr_array,axis=0)
    m0 = [np.trapz(water_yr_array[i,:], x=None, dx=1.0, axis=-1) for i in range(num_water_yrs)]
    m1 = [np.trapz(np.multiply(water_yr_array[i,:],range(365)), x=None, dx=1.0, axis=-1) for i in range(num_water_yrs)]
    CT = np.divide(m1,m0) + cst.day_of_year_oct1
    return CT

def get_metadata(file_nm):
    """Add metadata to plot
    """
    import time as timetool, os.path
    textstr = ('Willamette Water 2100' + 
              '\n' + '  Graph generated on ' + str(datetime.date.today()) +
              '\n' + '  File: ' + file_nm +\
              '\n' + '  Data generated on ' + timetool.ctime(os.path.getctime(file_nm))
              )
    return textstr

#functions for Recreational reservoirs plot

def get_recreational_reservoirs():
    """ Returns tuple of data for recreational reservoir locations"""
# Lat/long of 11 locations:
    reservoirs= {
            'Detroit':                  (-122.250739, 44.721682, 1, 'Detroit'),
            'Fern Ridge':               (-123.301178, 44.120915, 2, 'Fern_Ridge'),
            'Foster':                   (-122.641251, 44.414983, 3, 'Foster'),
            'Green Peter':              (-122.548650, 44.449654, 4, 'Green_Peter'),
            'Dorena':                   (-122.955039, 43.786775, 5, 'Dorena'),
            'Fall Creek':               (-122.739280, 43.951271, 6, 'Fall_Creek'),
            'Cottage_Grove':            (-123.052858, 43.716259, 7, 'Cottage_Grove'),
            'Blue River':               (-122.279801, 44.182290, 8, 'Blue_River'),
            'Hills Creek':              (-122.423156, 43.676881, 9, 'Hills_Creek'),
            'Lookout Point':            (-122.752465, 43.914625, 10, 'Lookout_Point'),
            'Cougar':                   (-122.231298, 44.107187, 11, 'Cougar')
            }
    return reservoirs

def get_scenarios():     
    scenarios = {
            'Reference':                '_Ref_',
            'HighClim':                 '_HighClim_',
            'LowClim':                  '_LowClim_',
            'HighPop':                  '_HighPop_',
            'UrbExpand':                '_UrbExpand_',
            'FireSuppress':             '_FireSuppress_',
            'FullCostUrb':              '_FullCostUrb_',
            'Managed':                  '_Managed_',
            'NoResorvoirs':             '_NoReservoirs_',
            'NoGrow':                   '_NoGrow_',
            'LateRefill':               '_LateRefill_',
            'AllFallow':                '_AllFallow_'
            }
    return scenarios

def get_visits():
    # list of 2-D arrays cantaining 2010 base visits during June, July, and August of 2010
    base_visits = [[2246,3048,2727],[1390,1886,1688],[891,1210,1082],[442,600,537],[275,373,333],
                   [145,197,176],[175,237,212],[165,224,200],[87,118,105],[39,54,48],[5,6,6]]
    visits_array_list = []
    visits_array = [[0 for j in range(365)] for i in range(89)]
    for r in range (len(base_visits)):
        for y in range(89):
            for d in range(365):
                if d in range(244,274):
                    visits_array[y][d] = base_visits[r][0]
                elif d in range(274,305):
                    visits_array[y][d] = base_visits[r][1]
                elif d in range(305,336):
                    visits_array[y][d] = base_visits[r][2]
        visits_array_list.append(np.array(visits_array))
    return visits_array_list

def get_pop_index(data):
    year_index = []
    year_index =[data[i+2,3]/data[2,3] for i in range(len(data[2:,3]))]
    return year_index
    
# used for determining the scenario of the population index
# based on the original scenario
def get_pop_scenario(scenario):
    if scenario == '_HighPop_':
        return '_HighPop_'
    elif scenario == '_NoGrow_':
        return '_NoGrow_'
    else:
        return '_Ref_'
#
    
def write_tinyfigs(datalist,figsize,mind,maxd,redblue, num_yrs,
                facecolor='0.8',linewidth = 1.):
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



def interp(x_orig, data, start,stop,num):
    """Interpolate data, returning both x and y values as floats
    """
    x = np.linspace(start,stop,num)
    y = np.interp(x,x_orig,data)
    return x, y

def colorline(x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0), linewidth=3, alpha=1.0,maxd=1,mind=0):
    '''
    Plot a colored line with coordinates x and y
    Specify colors in the array = y (could be some other array)
    Optionally specify a colormap, a norm function and a line width
    '''
 # modified from http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb    

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)   
    lc = LineCollection(segments, array = y, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)
    
    return lc
        
     
        
def write_tinyfigs2(datalist,upper, lower,figsize,mind,maxd,redblue, num_yrs,
                facecolor='0.8',linewidth = 1.):
    """Write tiny figs to be plotted on map
    """
    from matplotlib import pyplot as plt
    
    if redblue[0] == 'red':
        cmap = ListedColormap(['b','r'])
    else:
        cmap = ListedColormap(['r','b'])
    # Create a 'norm' (normalizing function) which maps data values to the interval [0,1]:
    norm = BoundaryNorm([-1e-3, 0, 1.e-3], cmap.N)  # cmap.N is number of items in the colormap
    
    for i in range(len(datalist)):
        plt.figure(figsize = figsize[i])
        plt.axis('off')
        plt.ylim( (mind,maxd) )
        x,y = interp(range(num_yrs), datalist[i], 0.,float(num_yrs-1),3*num_yrs)
        plt.fill_between(range(num_yrs),upper[i], lower[i], facecolor='0.6',lw=0,alpha=1.)
        lc = colorline(x, y, z=y, cmap=cmap, norm=norm, linewidth=1.5,maxd=maxd,mind=mind)
        plt.gca().add_collection(lc)
        plt.xlim(0,num_yrs)
        plt.savefig('tinyfig'+str(i)+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
        plt.close()

    return


def write_legend(data,figsize,mind,maxd,redblue, num_yrs,ylabel,xlabel,
                facecolor='0.8',linewidth = 1.):
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
    
def write_legend2(data,upper,lower,figsize,mind,maxd,redblue, num_yrs,ylabel,xlabel,
                facecolor='0.8',linewidth = 1.,which_legend='subbasins'):
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
    plt.xlim(0,num_yrs)
    if redblue[0] == 'blue':
        cmap = ListedColormap(['r','b'])
    else:
        cmap = ListedColormap(['b','r'])
        
    norm = BoundaryNorm([-1e-3, 0, 1.e-3], cmap.N)  # cmap.N is number of items in the colormap
    x,y = interp(range(num_yrs), data, 0., float(num_yrs-1), 3*num_yrs)
    plt.fill_between(range(num_yrs),upper, lower, facecolor='0.6',lw=0,alpha=1.)
    lc = colorline(x, y, z=y, cmap=cmap, norm=norm, linewidth=linewidth,maxd=maxd,mind=mind)
    plt.gca().add_collection(lc)
    font = {'size':'9'}           
    mpl.rc('font', **font)
    plt.ylabel(ylabel, fontsize=6)
    axleg.text(-30., mind*1.5, xlabel, fontsize=6,
            verticalalignment='top')
    if which_legend == 'subbasins':
        plt.savefig('tinyfig'+'12'+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
    elif which_legend == 'EFs':
        plt.savefig('tinyfig'+'8'+'.png', format="png", dpi=300, bbox_inches='tight',transparent=True)
    plt.close()
    mpl.rcdefaults()

    return
    
    
def write_map(title, lons, lats, file_graphics, textstr, shp, graphs=range(13), lons2=None, lats2=None):
    """Write the map
    """
    from matplotlib import pyplot as plt
    
    fig = plt.figure(figsize=(6,8))
    ax2 = fig.add_axes()
    plt.axes(frameon=False)
    
    WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
#        im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
    im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
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

    if lons2 is not None:         # if lons2 has a value
        x2,y2=WBmap(lons2,lats2)
        WBmap.scatter(x2, y2, marker='o',  s=50, lw=0,c='k')

    plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
    plt.close()       

    return

###############################################################################
###############################################################################
###############################################################################
# Map boundaries
lat_bounds = 43.31342817420548, 45.84870876153576
long_bounds = -121.401130054521,-124.151784119791

shp = 'C:\\code\\maplot\\shpf\\Sub_Area_gc'
png_path = 'C:\\code\\maplot pngs\\'
data_path = 'C:\\code\\maplot data\\'

figsize=[(0.8,0.6) for i in range(11)]
figsize.append((0.8,0.6))
figsize_leg = (0.8,0.6)

subbasins_loop = True
reservoirs_loop = False
correlations_loop = False
recreational_reservoirs_loop = True#edit here

subbasin_data, scenarios, scenarios_own, SimulatedHistoric = get_data()
file_baseline = '_Ref_'
baseline_case = 'Reference'
file_high = '_Extreme_'
file_low = '_LowClim_'
file_historical = '_HistoricRef_'

plots_to_plot = []

if subbasins_loop:
    
    subbasin_data_list = [subbasin_data[key] for key in subbasin_data]
    subbasin_data_list = sorted(subbasin_data_list,key=lambda x: x[2])  # order list by column number
    subbasin_data_lons = [subbasin_data_list[i][4] for i in range(len(subbasin_data_list))]
    subbasin_data_lats = [subbasin_data_list[i][5] for i in range(len(subbasin_data_list))]
    subbasin_data_order = [subbasin_data_list[i][2] for i in range(len(subbasin_data_list))]
    subbasin_data_area = [subbasin_data_list[i][3] for i in range(len(subbasin_data_list))]
    subbasin_data_climate_col = [subbasin_data_list[i][6] for i in range(len(subbasin_data_list))]
    subbasin_data_snow_col = [subbasin_data_list[i][7] for i in range(len(subbasin_data_list))]
    subbasin_data_ET_col = [subbasin_data_list[i][8] for i in range(len(subbasin_data_list))]
    
    lons = subbasin_data_lons
    lons[11]=subbasin_data_lons[11]+0.2
    lons.append(-123.7)
    lats = subbasin_data_lats
#    lats.append(43.9)
    lats.append(45.55)

#    plots_to_plot = range(4)
#    plots_to_plot.extend([9])
#    plots_to_plot.extend([4,45,5,8,9])
    plots_to_plot.extend([4])
    
if reservoirs_loop:
#    plots_to_plot.extend([101,102,103])
    plots_to_plot.extend([103])

    EFdata, DamLocs = get_EFdata()
    res_data_list = [EFdata[key] for key in EFdata]
    res_data_list = sorted(res_data_list, key=lambda x: x[2])  # order list by number
    res_data_lons = [res_data_list[i][0] for i in range(len(res_data_list))]
    res_data_lats = [res_data_list[i][1] for i in range(len(res_data_list))]
    res_data_order = [res_data_list[i][2] for i in range(len(res_data_list))]
    res_data_file = [data_path + res_data_list[i][3] for i in range(len(res_data_list))]
    res_data_EF_col = [res_data_list[i][4] for i in range(len(res_data_list))]
    
    EFlons = res_data_lons
    EFlats = res_data_lats
    EFlons.append(-123.7)
#1    EFlats.append(43.9)
    EFlats.append(45.55)
    
    dam_data_list = [DamLocs[key] for key in DamLocs]
    dam_data_lons = [dam_data_list[i][0] for i in range(len(dam_data_list))]
    dam_data_lats = [dam_data_list[i][1] for i in range(len(dam_data_list))]
    
if correlations_loop:
    plots_to_plot.extend([212,211])
    significance_cutoff = 0.1
    snt = imp.load_source('get_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
    snt = imp.load_source('basin_index_doy','C:\\code\\usgs-gauges\\snowroutines.py')
    snt = imp.load_source('cummulative_positive_wy_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
    snt = imp.load_source('MaxSWE_wy_snow_data','C:\\code\\usgs-gauges\\snowroutines.py')
    gg = imp.load_source('get_avg_discharge_by_moy','C:\\code\\usgs-gauges\\gageroutines.py')    
    gg = imp.load_source('get_avg_discharge_by_month','C:\\code\\usgs-gauges\\gageroutines.py')    
    gg = imp.load_source('get_gage_info','C:\\code\\usgs-gauges\\gageroutines.py')
    gg = imp.load_source('gage_data_filtered', 'C:\\code\\usgs-gauges\\gageroutines.py')
    gg = imp.load_source('reassign_by_yr','C:\\code\usgs-gauges\\gageroutines.py')
    pp = imp.load_source('get_precip_data','C:\\code\\usgs-gauges\\preciproutines.py')
    pp = imp.load_source('get_precip_by_moyrange','C:\\code\\usgs-gauges\\preciproutines.py')
    pp = imp.load_source('reassign_by_wyr','C:\\code\\usgs-gauges\\preciproutines.py')
    pp = imp.load_source('basin_index','C:\\code\\usgs-gauges\\preciproutines.py')
            
    allDamLocs = get_allDamLocs()
    Dam_data_list = [allDamLocs[key] for key in allDamLocs]
    Dam_data_list = sorted(Dam_data_list, key=lambda x: x[2])  # order list by number
    Dam_lons = [Dam_data_list[i][0] for i in range(len(Dam_data_list))]
    Dam_lats = [Dam_data_list[i][1] for i in range(len(Dam_data_list))]

if recreational_reservoirs_loop:# resorvoir and scenario information/data
    #plots_to_plot.extend([301])

    reservoirs = get_recreational_reservoirs()
    Dam_data_list = [reservoirs[key] for key in reservoirs]
    Dam_data_list = sorted(Dam_data_list, key=lambda x: x[2])  # order list by number
    Dam_lons = [Dam_data_list[i][0] for i in range(len(Dam_data_list))]
    Dam_lats = [Dam_data_list[i][1] for i in range(len(Dam_data_list))]
    
    scenarios = get_scenarios()
    scenarios_list = [scenarios[key] for key in scenarios]
    
    
print 'Plots to be plotted are:', '\t', plots_to_plot
for plot_num in plots_to_plot:

        
############  Summer reservoir welfare losses w mini figs/LINES & SHADING ############    
    if plot_num == 4:
        plt.close()
        ########## Test code
        print "Test"
        visits_data = get_visits()
        
        for r in range(len(Dam_data_list)):
            sum_s = [0 for s in range(len(scenarios_list))]         
            
            for s in range(len(scenarios_list)):# do for each scenario
                sum_s[s]
                pop_file = data_path + 'WB_Population' + get_pop_scenario(scenarios_list[s]) + 'Run0.csv'
                pop_data = get_pop_index(np.array(np.genfromtxt(pop_file,delimiter=',',skip_header=1)))
                ele_file = data_path + Dam_data_list[r][3] + '_Reservoir_(USACE)_Reservoir' + scenarios_list[s] + 'Run0.csv'#temporary
                ele_data = mfx(ele_file,column=1,skip=cst.day_of_year_oct1)
                ele_full = np.amax(ele_data,axis=1)
                sum_y = [0 for y in range(89)]# sum for the year
                
                for y in range(89):
                    full_less_current = (ele_full[y]*np.ones_like(ele_data[y])) - ele_data[y]
                    for d in range(365):
                        an = (-0.165)*visits_data[0][y][d]*pop_data[y]*full_less_current[d]
                        sum_y[y] = sum_y[y] + an
                    sum_s[s] = sum_s[s] + sum_y[y]
            print "\n" + Dam_data_list[r][3]
            print sum_s

        ####################
        """
        window = binomial_window(15)
        file_nm = data_path + 'Discharge_(Subbasins)'+file_baseline+'Run0.csv'    
        # Calculate Baselines
        baseline = {}
        Q10 = {}
        for key in SimulatedHistoric:
            data_hd1=[mfx(file_nm.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                       movingaveragevec=np.ones(30)/30.) for i in range(12)]
            data_hd1[7] = data_hd1[7] - data_hd1[8]  # correct N Santiam for S Santiam contribution
            Q10.update({key:[np.percentile(data_hd1[i][0:59,:], 10.,axis=0) for i in range(12)]})
            data_hd_binary = [compare_rows(data_hd1[i],Q10[key][i]) for i in range(12)]  #1's are drought
            summer_dr_d = [np.sum(data_hd_binary[i][:,260:365],1) for i in range(12)]
            baseline.update({key:[np.mean(summer_dr_d[i]) for i in range(12)]})  
        
        data_to_stack = []
        for key in scenarios:
            data_hd1=[mfx(file_nm.replace(file_baseline+'Run0',scenarios[key]), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                       movingaveragevec=np.ones(30)/30.) for i in range(12)]
            data_hd1[7] = data_hd1[7] - data_hd1[8]  # correct N Santiam for S Santiam contribution
            data_hd_binary = [compare_rows(data_hd1[i],Q10[scenarios_own[key]][i]) for i in range(12)]  #1's are drought
            summer_dr_d = [np.sum(data_hd_binary[i][:,260:365],1) for i in range(12)]
            data_to_stack.append([np.subtract(movingaverage(summer_dr_d[i],window), baseline[scenarios_own[key]][i]) for i in range(12)])  
            # Calculate baseline-subtracted value
            if key == baseline_case:
                summer_dr_d_smthd = [np.subtract(movingaverage(summer_dr_d[i],window), baseline[scenarios_own[key]][i]) for i in range(12)]
        
        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(12)] 
        upper = [np.max(data_stacked[i],1) for i in range(12)]
        lower = [np.min(data_stacked[i],1) for i in range(12)]
        
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        xctr = 0.5
        yctr = 0.5
        
        redblue = ['red','blue']
        num_yrs = len(summer_dr_d_smthd[0])
        write_tinyfigs2(summer_dr_d_smthd,upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, Drought\,$ [days]'
        xlabel = 'Red = Drier'
        write_legend2(summer_dr_d_smthd[11], upper[11], lower[11],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
               
        title = "Change in Summer Hydrologic Drought"
        file_graphics = 'change_in_drought_days_wGrphs.png'
        
        graphs = range(13); graphs.remove(11)

        write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs=graphs)
"""