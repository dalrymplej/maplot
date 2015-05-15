
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
import xlrd
from scipy import stats

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

subbasins_loop = False 
reservoirs_loop = False
correlations_loop = True

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
    plots_to_plot.extend([0])
    
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
    
    # Read a parameter file in xls format.
    Q_SWE_PRE_params = xlrd.open_workbook('Q-SWE-PRE.xlsx')
    Gauge_num = Q_SWE_PRE_params.sheet_by_index(2).col_values(0)[1:]
    Gauge_loc = Q_SWE_PRE_params.sheet_by_index(2).col_values(1)[1:]
    c_Lats = Q_SWE_PRE_params.sheet_by_index(2).col_values(5)[1:]
    c_Longs = Q_SWE_PRE_params.sheet_by_index(2).col_values(6)[1:]
    Q_SWE0 = Q_SWE_PRE_params.sheet_by_index(2).col_values(7)[1:]
    Delta_Q_SWE1 = Q_SWE_PRE_params.sheet_by_index(2).col_values(8)[1:]
    Q_SWE1 = Q_SWE_PRE_params.sheet_by_index(2).col_values(9)[1:]
    R2_SWE = Q_SWE_PRE_params.sheet_by_index(2).col_values(10)[1:]
    p_value_SWE = Q_SWE_PRE_params.sheet_by_index(2).col_values(11)[1:]
    SWE_frac = Q_SWE_PRE_params.sheet_by_index(2).col_values(12)[1:]
    
    Q_PRE0 = Q_SWE_PRE_params.sheet_by_index(2).col_values(17)[1:]
    Delta_Q_PRE1 = Q_SWE_PRE_params.sheet_by_index(2).col_values(18)[1:]
    Q_PRE1 = Q_SWE_PRE_params.sheet_by_index(2).col_values(19)[1:]
    R2_PRE = Q_SWE_PRE_params.sheet_by_index(2).col_values(20)[1:]
    p_value_PRE = Q_SWE_PRE_params.sheet_by_index(2).col_values(21)[1:]
    PRE_frac = Q_SWE_PRE_params.sheet_by_index(2).col_values(22)[1:]
    
    num_gauge = len(Q_SWE0)
    c_Lats_SWE = list(c_Lats)  # need to do it this way because of aliasing
    c_Longs_SWE = list(c_Longs)
    for i in range(num_gauge-1,-1,-1): # count back from end of list
        c_Longs_SWE[i] = -1*c_Longs_SWE[i]
        if SWE_frac[i] < 0.: SWE_frac[i] = 0.
        if Q_SWE0[i] == '' or Delta_Q_SWE1[i] == '':   # delete parts of list that are empty
            del(c_Lats_SWE[i])
            del(c_Longs_SWE[i])
            del(Q_SWE0[i])
            del(Delta_Q_SWE1[i])
            del(Q_SWE1[i])
            del(R2_SWE[i])
            del(p_value_SWE[i])
            del(SWE_frac[i])
    num_gauge_SWE = len(Q_SWE0)
    
    c_Lats_PRE = list(c_Lats)
    c_Longs_PRE = list(c_Longs)
    for i in range(num_gauge-1,-1,-1): # count back from end of list
        c_Longs_PRE[i] = -1*c_Longs_PRE[i]
        if PRE_frac[i] < 0.: PRE_frac[i] = 0.
        if Q_PRE0[i] == '' or Delta_Q_PRE1[i] == '':   # delete parts of list that are empty
            del(c_Lats_PRE[i])
            del(c_Longs_PRE[i])
            del(Q_PRE0[i])
            del(Delta_Q_PRE1[i])
            del(Q_PRE1[i])
            del(R2_PRE[i])
            del(p_value_PRE[i])
            del(PRE_frac[i])
    num_gauge_PRE = len(Q_PRE0)
    
    significance_cutoff = 0.4
    Q_SWE1_sig = list(Q_SWE1)
    SWE_frac_sig = list(SWE_frac)
    for i in range(num_gauge_SWE-1,-1,-1): # count back from end of list
        if p_value_SWE[i] > significance_cutoff:   # zero out parts of list that are not significant
            SWE_frac_sig[i] = 0.
    Q_PRE1_sig = Q_PRE1
    PRE_frac_sig = PRE_frac
    for i in range(num_gauge_PRE-1,-1,-1): # count back from end of list
        if p_value_PRE[i] > significance_cutoff:   # zero out parts of list that are not significant
            PRE_frac_sig[i] = 0.

    SWEPRE_range = SWE_frac_sig + PRE_frac_sig
    
    subbasin_data_list = [subbasin_data[key] for key in subbasin_data]
    subbasin_data_list = sorted(subbasin_data_list,key=lambda x: x[2])  # order list by column number
    subbasin_data_lons = [subbasin_data_list[i][4] for i in range(len(subbasin_data_list))]
    subbasin_data_lats = [subbasin_data_list[i][5] for i in range(len(subbasin_data_list))]
    subbasin_data_order = [subbasin_data_list[i][2] for i in range(len(subbasin_data_list))]
    subbasin_data_area = [subbasin_data_list[i][3] for i in range(len(subbasin_data_list))]
    subbasin_data_climate_col = [subbasin_data_list[i][6] for i in range(len(subbasin_data_list))]
    subbasin_data_snow_col = [subbasin_data_list[i][7] for i in range(len(subbasin_data_list))]
    subbasin_data_ET_col = [subbasin_data_list[i][8] for i in range(len(subbasin_data_list))]
    
    plots_to_plot.extend([204])
    

print 'Plots to be plotted are:', '\t', plots_to_plot
for plot_num in plots_to_plot:
    
    
############  Specific Discharge ############    
    if plot_num == 0: 
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        plt.title("Specific Discharge & Jul - Aug Discharge")
        file_nm = data_path + 'Discharge_(Subbasins)'+file_baseline+'Run0.csv'
        data1=[mfx(file_nm,column=subbasin_data_order[i],skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data1_spQ=[np.mean(data1[i])/subbasin_data_area[i]*cst.seconds_in_yr*100. for i in range(12)]
        summer_Q = [nrc(data1[i],[1,273],[88,335]) for i in range(12)]  # Start of summer = day 260, end = day 350
        
        import heapq
        data1_2nd_lgst = heapq.nlargest(2, summer_Q)[1]  #find second-largest number
        data1_size = np.clip(200.*np.array(summer_Q)/data1_2nd_lgst,15.,20000.)
        
        colord = np.array(data1_spQ)
        
        x,y=WBmap(subbasin_data_lons[:12],subbasin_data_lats[:12])
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','blue'],128)
        m = WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        # add colorbar.
        cbar = WBmap.colorbar(m, location = 'bottom', pad='6%', size='3%')#,location='bottom',pad="5%",size='8')
        cbar.set_label('annual specific discharge (cm/y)',size=10)
        cbar.ax.tick_params(labelsize=9) 
        
        file_graphics = 'spQ.png'     
        plt.text(0., 0, get_metadata(file_nm), fontsize=3,
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
        im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Summer Hydrologic Drought")
        
        file_nm = data_path + 'Discharge_(Subbasins)'+file_baseline+'Run0.csv'

        data1=[mfx(file_nm, column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd1 = data1
        
        data1=[mfx(file_nm.replace(file_baseline,file_high), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd2 = data1
        
        data1=[mfx(file_nm.replace(file_baseline,file_low), column=subbasin_data_order[i], skip=cst.day_of_year_oct1,
                   movingaveragevec=np.ones(30)/30.) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        data_hd3 = data1
        
        data_avg = [(data_hd1[i]+data_hd2[i]+data_hd3[i])/3. for i in range(12)]
        Q10 = [np.percentile(data_avg[i][0:10,:], 10.,axis=0) for i in range(12)]
        data_hd_binary = [compare_rows(data_avg[i],Q10[i]) for i in range(12)]  #1's are drought
        
        diff_drought_days = [
                       nrc(data_hd_binary[i],[69,260],[88,350], oper='sum') 
                    -  nrc(data_hd_binary[i],[0, 260],[19,350], oper='sum') 
                    for i in range(12)]  #+ve numbers are increasing drought
       
        colord = np.array(diff_drought_days)
        
        x,y=WBmap(subbasin_data_lons[:12],subbasin_data_lats[:12])
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['blue','white','red'],128)
        WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'drought_days.png'        
        plt.text(0., 0, get_metadata(file_nm), fontsize=3,
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
        im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Annual Precipitation")
        
        file_nm = data_path + 'Climate_(Subbasin)'+file_baseline+'Run0.csv'
        data1=[mfx(file_nm, column=subbasin_data_climate_col[i], skip=cst.day_of_year_oct1) for i in range(11)]
        file_nmWB = data_path + 'Climate'+file_baseline+'Run0.csv'
        data1.append(mfx(file_nmWB, column=subbasin_data_climate_col[11], skip=cst.day_of_year_oct1))
        data_hd1 = data1
        
        diff_ann_precip = [
                    + nrc(data_hd1[i],[0,0],[19,364], oper='avg') 
                    - nrc(data_hd1[i],[69, 0],[88,364], oper='avg') 
                    for i in range(12)]  # +ve numbers are decreasing precip
        print nrc(data_hd1[0],[0,0],[19,364], oper='avg')
        print nrc(data_hd1[0],[69, 0],[88,364], oper='avg')
        print diff_ann_precip
       
        colord = np.array(diff_ann_precip)
        
        x,y=WBmap(subbasin_data_lons[:12],subbasin_data_lats[:12])
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['blue','white'],128)
        WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'diff_ann_precip.png'        
        plt.text(0., 0, get_metadata(file_nm), fontsize=3,
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
        im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        
        plt.title("Change in Winter (Nov 1 - Mar 31) Temp")
        
        file_nm = data_path + 'Climate_(Subbasin)'+file_baseline+'Run0.csv'
        data1=[mfx(file_nm, column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1) for i in range(11)]
        file_nmWB = data_path + 'Climate'+file_baseline+'Run0.csv'
        data1.append(mfx(file_nmWB, column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
        data_hd1 = data1
        
        diff_winter_temp = [
                      nrc(data_hd1[i],[69,31],[88,182], oper='avg') 
                    - nrc(data_hd1[i],[0, 31],[19,182], oper='avg') 
                    for i in range(12)]  #+ve numbers are increasing temp
        print 'early cent', '\t',nrc(data_hd1[i],[69,31],[88,182], oper='avg')
        print 'late cent', '\t',nrc(data_hd1[i],[0, 31],[19,182], oper='avg')
        print np.array(diff_winter_temp)
       
        colord = np.array(diff_winter_temp)
        
        x,y=WBmap(subbasin_data_lons[:12],subbasin_data_lats[:12])
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',['white','red'],128)
        WBmap.scatter(x, y, marker='o',  s=200., lw=0,c=colord,cmap = cmap1)
        
        file_graphics = 'diff_winter_Temp.png'        
        plt.text(0., 0, get_metadata(file_nm), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=300, bbox_inches='tight')
        plt.close()       




############  Summer Hydrologic Drought w mini figs/LINES & SHADING ############    
    elif plot_num == 4:
        plt.close()
        
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


############  Water Deficit w mini figs/LINES & SHADING ############    
    elif plot_num == 45:
        plt.close()
        
        window = binomial_window(15)
        file_nm = data_path + 'ET_by_Subbasin'+file_baseline+'Run0.csv'    
        file_ex = data_path + 'ET_by_Elevation_(mm)'+file_baseline+'Run0.csv' # Need average for whole WB, in different file
        # Calculate Baseline
        baseline = {}
        for key in SimulatedHistoric:
            data_ET=[mfx(file_nm.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=subbasin_data_ET_col[i], 
                         skip=cst.day_of_year_oct1) for i in range(12)]
            data_PET=[mfx(file_nm.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=subbasin_data_ET_col[i]+1, 
                         skip=cst.day_of_year_oct1) for i in range(12)]
            data_ET[11] =mfx(file_ex.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=1, 
                         skip=cst.day_of_year_oct1)
            data_PET[11]=mfx(file_ex.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=2, 
                         skip=cst.day_of_year_oct1)
            data_hd1 = [data_PET[i] - data_ET[i] for i in range(12)]
            wd1 = [np.sum(data_hd1[i][:,:],1) for i in range(12)]
            baseline.update({key:[np.ones(89)*np.average(wd1[i]) for i in range(12)]})
                
        data_to_stack = []
        for key in scenarios:
            data_ET=[mfx(file_nm.replace(file_baseline+'Run0',scenarios[key]), column=subbasin_data_ET_col[i], 
                         skip=cst.day_of_year_oct1) for i in range(12)]
            data_PET=[mfx(file_nm.replace(file_baseline+'Run0',scenarios[key]), column=subbasin_data_ET_col[i]+1, 
                         skip=cst.day_of_year_oct1) for i in range(12)]
            data_ET[11] =mfx(file_ex.replace(file_baseline+'Run0',scenarios[key]), column=1, 
                         skip=cst.day_of_year_oct1)
            data_PET[11]=mfx(file_ex.replace(file_baseline+'Run0',scenarios[key]), column=2, 
                         skip=cst.day_of_year_oct1)
            data_hd1 = [data_PET[i] - data_ET[i] for i in range(12)]
            wd1 = [np.sum(data_hd1[i][:,:],1) for i in range(12)]
            wd1_smthd = [np.subtract(movingaverage(wd1[i],window), baseline[scenarios_own[key]][i])[8:83] for i in range(12)]
            data_to_stack.append([wd1_smthd[i] for i in range(12)]) 
            # Calculate baseline-subtracted value
            if key == baseline_case:
                    wd_smthd = [np.subtract(movingaverage(wd1[i],window), baseline[scenarios_own[key]][i])[8:83] for i in range(12)]
        
        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(12)] 
        upper = [np.max(data_stacked[i],1) for i in range(12)]
        lower = [np.min(data_stacked[i],1) for i in range(12)]
        
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        xctr = 0.5
        yctr = 0.5
        
        redblue = ['red','blue']
        num_yrs = len(wd1_smthd[0])
        write_tinyfigs2(wd_smthd,upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, Deficit\,$ [mm]'
        xlabel = 'Red = Drier'
        write_legend2(wd_smthd[11], upper[11], lower[11],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
               
        title = "Change in Water Deficit"
        file_graphics = 'change_in_water_deficit_wGrphs.png'
        
        graphs = range(13); graphs.remove(11)

        write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs=graphs)



############  Winter Temperature w mini figs ############    
    elif plot_num == 5:
        plt.close()
        window = binomial_window(15)
        file_nm = data_path + 'Climate_(Subbasin)'+file_baseline+'Run0.csv'
        file_nmWB = data_path + 'Climate'+file_baseline+'Run0.csv'
       
        # Calculate Baseline
        baseline = {}
        for key in SimulatedHistoric:
            data_hd1=[mfx(file_nm.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1) for i in range(11)]
            data_hd1.append(mfx(file_nmWB.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
            data_winter = [data_hd1[i][:,29:182] for i in range(12)]
            baseline.update({key:[np.mean(data_winter[i]) for i in range(12)]})  # avg over winter each year for ea subbasin
                       
        data_to_stack = []
        for key in scenarios:
            data_hd1=[mfx(file_nm.replace(file_baseline+'Run0',scenarios[key]), column=subbasin_data_climate_col[i]+1, skip=cst.day_of_year_oct1) for i in range(11)]
            data_hd1.append(mfx(file_nmWB.replace(file_baseline+'Run0',scenarios[key]), column=subbasin_data_climate_col[11]-1, skip=cst.day_of_year_oct1))
            data_winter = [data_hd1[i][:,29:182] for i in range(12)]
            winter_tmps = [np.mean(data_winter[i],1) for i in range(12)]  # avg over winter each year for ea subbasin
            winter_temps_smthd1 = [np.subtract(movingaverage(winter_tmps[i],window), baseline[scenarios_own[key]][i])[8:83] for i in range(12)]
            data_to_stack.append([winter_temps_smthd1[i] for i in range(12)])  
            # Calculate baseline-subtracted value
            if key == baseline_case:
                winter_temps_smthd = [np.subtract(movingaverage(winter_tmps[i],window), baseline[scenarios_own[key]][i])[8:83] for i in range(12)]
                
        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(12)] 
        upper = [np.max(data_stacked[i],1) for i in range(12)]
        lower = [np.min(data_stacked[i],1) for i in range(12)]
        
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        xctr = 0.5
        yctr = 0.5

        redblue = ['red','blue']
        num_yrs = len(winter_temps_smthd[0])
        write_tinyfigs2(winter_temps_smthd,upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, Temp\,$ [$^{\circ}\mathrm{C}$]'
        xlabel = 'Red = Warmer'
        write_legend2(winter_temps_smthd[11], upper[11], lower[11],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
        
        title = "Change in Winter Temperatures (Nov - Mar)"
        file_graphics = 'change_in_winter_temp_wGrphs.png'
        
        graphs = range(13); graphs.remove(11)

        write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs = graphs)


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
            
            write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs=graphs)
            
#            assert False
            
            
            
            
            
############  Econ w mini figs w lines & shading ############    
    elif plot_num == 60:
        plt.close()
        file_types = ['subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv', 
                      'subbasin_tot_ac_of_developed_land_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_ac_of_forest_land_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_ag_land_values_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_ag_land_values_irrigable_GW_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_ag_land_values_irrigable_SW_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_dev_land_values_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_forest_land_values_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_LR_farm_rent_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_LR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_LR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_SR_farm_rent_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_SR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv',
                      'subbasin_tot_SR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv',
                      ]
        
        for subfiletype in file_types:
            econ_fileswopath = [eachfile.partition(data_path)[2] for eachfile in econ_files]            
            econ_files = getfilenames(data_path,'subbasin')

            file_nm = data_path + subfiletype
            data_to_stack = []
            title = file_nm.partition(data_path)[2][:-13]
            png_file_nm = title+'.png'
            for key in scenarios:
                data_v = np.array(np.genfromtxt(file_nm.replace('_Ref_Run0',scenarios[key]), delimiter=',',skip_header=1))
                data1 = [data_v[2:,subbasin_data_order[i]+1] for i in range(11)]
                data1.append(data_v[2:,1])
                baseline = [data1[i][0] for i in range(11)]
                data1 = [np.subtract(data1[i],baseline[i]) for i in range(11)]
                data_to_stack.append([data1[i] for i in range(11)])  
           
            data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(11)]
            data_stacked = [np.column_stack(data_to_stack[i]) for i in range(11)] 
            upper = [np.max(data_stacked[i],1) for i in range(11)]
            lower = [np.min(data_stacked[i],1) for i in range(11)]
                
            maxd = np.max(np.array([np.max(upper[i]) for i in range(11)]))
            mind = np.min(np.array([np.min(lower[i]) for i in range(11)]))
            if maxd >= abs(mind):
                xctr = 0.75
                yctr = 0.5
            else:
                xctr = 0.75
                yctr = 0.7
            redblue = ['red','blue']
            num_yrs = len(data1[0])
            write_tinyfigs2(data1, upper, lower, figsize,
                            mind,maxd,redblue, num_yrs, facecolor = '0.6',
                            linewidth = 1.5)
            
            ylabel = r'$\Delta \, value\,$'
            xlabel = ' '
            write_legend2(data1[4], upper[4], lower[4],figsize_leg,
                          mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                          linewidth=1.5)
            
            file_graphics = png_file_nm        
    
            graphs = range(11)
            write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs=graphs)
                
#            assert False
            
            
            
            
            
############  Econ w mini figs normalized by land area ############    
    elif plot_num == 7:
        plt.close()
        run_names = [
        ('subbasin_tot_LR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_SR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_LR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_SR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_LR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_SR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv')
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
                write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs=graphs)
                
#                assert False
            
            
            
            
############  Econ w mini figs normalized by land area ############    
    elif plot_num == 70:
        plt.close()
        run_names = [
        ('subbasin_tot_LR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_SR_farm_rent_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_ag_land_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_LR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_SR_farm_rent_irrigable_GW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_GW_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_LR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv'),
        ('subbasin_tot_SR_farm_rent_irrigable_SW_by_SUB_AREA_Ref_Run0.csv','subbasin_tot_ac_of_irrigable_ag_land_SW_by_SUB_AREA_Ref_Run0.csv')
        ]
        
            
        for files in run_names:
            data_to_stack = []
            title = files[0][:-13]
            print title
            for key in scenarios:
                files_scen = (files[0].replace(scenarios['Reference'],scenarios[key]),files[1].replace(scenarios['Reference'],scenarios[key]))
                file_nm_num = data_path + files_scen[0]
                file_nm_denom = data_path + files_scen[1]
                file_nmWB = file_nm_num     
                png_file_nm = title+'_divided_by_area'+'.png'
                data_v_num = np.array(np.genfromtxt(file_nm_num, delimiter=',',skip_header=1)) # Read csv file
                data_v_denom = np.array(np.genfromtxt(file_nm_denom, delimiter=',',skip_header=1)) # Read csv file
                data1_num = [data_v_num[2:,subbasin_data_order[i]+1] for i in range(11)]
                data1_denom = [data_v_denom[2:,subbasin_data_order[i]+1] for i in range(11)]
#                data1_num.append(data_v_num)
#                data1_denom.append(data_v_denom)
                data1 = [np.divide(data1_num[i],data1_denom[i]) for i in range(11)]
                data1 = [np.subtract(data1[i],data1[i][0]) for i in range(11)]
                data_to_stack.append([data1[i] for i in range(11)])  
                
            data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(11)]
            
            data_stacked = [np.column_stack(data_to_stack[i]) for i in range(11)] 
            upper = [np.max(data_stacked[i],1) for i in range(11)]
            lower = [np.min(data_stacked[i],1) for i in range(11)]
            
            maxd = np.max(np.array([np.max(upper[i]) for i in range(11)]))
            mind = np.min(np.array([np.min(lower[i]) for i in range(11)]))
            if maxd >= abs(mind):
                xctr = 0.75
                yctr = 0.5
            else:
                xctr = 0.75
                yctr = 0.7
                
            redblue = ['red','blue']
            num_yrs = len(data1[0])
            write_tinyfigs2(data1,upper, lower, figsize, mind,maxd,redblue, 
                            num_yrs, facecolor='0.6', linewidth = 1.5)
            
            ylabel = r'$\Delta \, Value\,$' +r'[\$/ac]'
            xlabel = ' '
            write_legend2(data1[4],upper[4], lower[4], figsize_leg,
                          mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                          linewidth=1.5)
            
            file_graphics = png_file_nm        
    
            graphs = range(11)
            graphs.append(12)
            write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs=graphs)
            
            
            
            
############  Center of Timing w mini figs ############    
    elif plot_num == 8:
        plt.close()
        window = binomial_window(15)
        file_nm = data_path + 'Discharge_(Subbasins)'+file_baseline+'Run0.csv'
               
        # Calculate Baseline
        baseline = {}
        for key in SimulatedHistoric:
            data1=[mfx(file_nm.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=subbasin_data_order[i], skip=cst.day_of_year_oct1) for i in range(12)]
            data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
            ctdata = [np.array(ct(data1[i])) for i in range(12)]
            baseline.update({key:[np.mean(ctdata[i]) for i in range(12)]})
        
        data_to_stack = []
        for key in scenarios:
            data1=[mfx(file_nm.replace(file_baseline+'Run0',scenarios[key]), column=subbasin_data_order[i], skip=cst.day_of_year_oct1) for i in range(12)]
            data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
            ctdata = [np.array(ct(data1[i])) for i in range(12)]
            delta_discharge_timing = [-1.*np.subtract(movingaverage(ctdata[i],window), baseline[scenarios_own[key]][i]) for i in range(12)]
            data_to_stack.append([delta_discharge_timing[i] for i in range(12)])  
            if key == baseline_case:
                delta_discharge_timing_baseline = np.array([delta_discharge_timing[i][8:83] for i in range(12)])

        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(12)] 
        upper = [np.max(data_stacked[i][8:83],1) for i in range(12)]
        lower = [np.min(data_stacked[i][8:83],1) for i in range(12)]
            
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        delta_discharge_timing = np.array([delta_discharge_timing[i][8:83] for i in range(12)])

        redblue = ['red','blue']
        num_yrs = len(delta_discharge_timing[0])
        write_tinyfigs2(delta_discharge_timing_baseline, upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, CT\,$ [days]'
        xlabel = 'Red = Earlier'
        write_legend2(delta_discharge_timing_baseline[11], upper[11], lower[11],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
            
        title = "Change in Timing of Discharge (CT)"
        file_graphics = 'change_in_discharge_timing_wGrphs.png'        
        graphs = range(13); graphs.remove(11)

        write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs=graphs)
            
            
            
            
############  Max SWE w mini figs ############    
    elif plot_num == 9:
        plt.close()

        window = binomial_window(15)
        figsize9=[(figsize[i][0],figsize[i][1]*1.5) for i in range(12)]
        figsize_leg9=(figsize_leg[0],figsize_leg[1]*1.5) 
        file_nm = data_path + 'Snow_(Subbasin)'+file_baseline+'Run0.csv'
        file_nmWB = data_path + 'Snow_(mm)'+file_baseline+'Run0.csv'
                
        # Calculate Baseline
        baseline = {}
        for key in SimulatedHistoric:
            data1=[mfx(file_nm.replace(file_baseline+'Run0',SimulatedHistoric[key]), column=subbasin_data_snow_col[i], 
                       skip=cst.day_of_year_oct1) for i in range(11)]
            data1.append(mfx(file_nmWB.replace(file_baseline+'Run0',SimulatedHistoric[key]), 
                             column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
            SWE1 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
            baseline.update({key:[np.mean(SWE1[i]) for i in range(12)]}) 
        
        data_to_stack = []
        for key in scenarios:
            data1=[mfx(file_nm.replace(file_baseline+'Run0',scenarios[key]), column=subbasin_data_snow_col[i], 
                       skip=cst.day_of_year_oct1) for i in range(11)]
            data1.append(mfx(file_nmWB.replace(file_baseline+'Run0',scenarios[key]), 
                             column=subbasin_data_snow_col[11], skip=cst.day_of_year_oct1))
            SWE1 = [np.max(data1[i],1)*subbasin_data_area[i]/10./subbasin_data_area[11] for i in range(12)]  # max SWE (cm) over winter each year for ea subbasin
            data_to_stack.append([np.subtract(movingaverage(SWE1[i],window), baseline[scenarios_own[key]][i]) for i in range(12)])  
            if key == baseline_case:
                SWE_smthd = [10.*np.subtract(movingaverage(SWE1[i],window), baseline[scenarios_own[key]][i]) for i in range(12)]  # plot in mm instead of cm

        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(12)]
        data_stacked = [10.*np.column_stack(data_to_stack[i]) for i in range(12)] #stack & convert to mm
        upper = [np.max(data_stacked[i][8:83],1) for i in range(12)]
        lower = [np.min(data_stacked[i][8:83],1) for i in range(12)]
            
        maxd = np.max(np.array([np.max(upper[i]) for i in range(12)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(12)]))
        SWE_smthd = [SWE_smthd[i][8:83] for i in range(12)]
        xctr = 0.5
        yctr = 0.75
        
        redblue = ['blue','red']
        num_yrs = len(SWE_smthd[0])
        write_tinyfigs2(SWE_smthd, upper, lower, figsize9,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, SWE\,$ [mm]'
        xlabel = 'Red = Less SWE'
        write_legend2(SWE_smthd[11], upper[11], lower[11],figsize_leg9,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5)
               
        
        title = "Change in Basin-Averaged Max SWE"
        file_graphics = 'change_in_max_SWE_wGrphs.png'        
        graphs = range(13); graphs.remove(11)

        write_map(title, lons, lats, file_graphics, get_metadata(file_nm), shp, graphs=graphs)

##############################################################################
#  ENVIRONMENTAL FLOWS        
############  BiOp & Env Flows w mini figs ############    
    elif plot_num == 101:
        plt.close()
        window = binomial_window(15)
        num_locs = len(res_data_list)
        figsize=[(1.1,0.8) for i in range(num_locs)]
        figsize.append((1.1,0.8))
        figsize_leg = (1.1,0.8)
                
        # Get EF & BiOp rules
        EFrules = get_EFrules()
        EF_rules_list = [EFrules[key] for key in EFrules]
        EF_rules_list = sorted(EF_rules_list, key=lambda x: x[0])  # order list by number
        EF_rules_list = [EF_rules_list[i][1] for i in range(num_locs)]
        
        # Calculate Baseline
        file_nm = res_data_file
        baseline = {}
        for key in SimulatedHistoric:
            data1=[mfx(file_nm[i].replace(file_baseline+'Run0',SimulatedHistoric[key]), column=res_data_EF_col[i], skip=cst.day_of_year_oct1) for i in range(num_locs)]
            num_yrs = np.shape(data1[0])[0]       
            viols1 = [RuleReliability(data1[i],num_yrs, EF_rules_list[i]) for i in range(num_locs)]  # num of rule violations per year
            baseline.update({key:[np.mean(viols1[i]) for i in range(num_locs)]})  
       
        # Calculate baseline-subtracted value        
        data_to_stack = []
        for key in scenarios:
            data1=[mfx(file_nm[i].replace(file_baseline+'Run0',scenarios[key]), column=res_data_EF_col[i], skip=cst.day_of_year_oct1) for i in range(num_locs)]
            num_yrs = np.shape(data1[0])[0]       
            viols1 = [RuleReliability(data1[i],num_yrs, EF_rules_list[i]) for i in range(num_locs)]  # num of rule violations per year
            data_to_stack.append([np.subtract(movingaverage(viols1[i],window), baseline[scenarios_own[key]][i]) for i in range(num_locs)])  
            if key == baseline_case:
                viols_smthd = [np.subtract(movingaverage(viols1[i],window), baseline[scenarios_own[key]][i]) for i in range(num_locs)]

        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(num_locs)]
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(num_locs)] 
        upper = [np.max(data_stacked[i][8:83],1) for i in range(num_locs)]
        lower = [np.min(data_stacked[i][8:83],1) for i in range(num_locs)]
            
        maxd = np.max(np.array([np.max(upper[i]) for i in range(num_locs)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(num_locs)]))
        viols_smthd = [viols_smthd[i][8:83] for i in range(num_locs)]
        xctr = 0.5
        yctr = 0.75
        
        redblue = ['blue','red']
        num_yrs = len(viols_smthd[0])
        write_tinyfigs2(viols_smthd, upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, EF \,Reliab\,$ [days]'
        xlabel = 'Red = less EF reliability'
        write_legend2(viols_smthd[0], upper[0], lower[0],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5, which_legend = 'EFs')
               
        
        title = "Reliability of BiOp and Environmental Flows"
        file_graphics = 'change_in_Biop-EF_reliability_wGrphs.png'        
        graphs = range(num_locs+1); graphs.remove(0)

        write_map(title, EFlons, EFlats, file_graphics, get_metadata(file_nm[0]), 
                  shp, graphs=graphs, lons2=dam_data_lons, lats2=dam_data_lats)
       



##############################################################################
#  ENVIRONMENTAL FLOWS        
############  BiOp & Env Flows w mini figs SUMMER ONLY ############    
    elif plot_num == 102:
        plt.close()
        window = binomial_window(15)
        num_locs = len(res_data_list)
        figsize=[(1.1,0.8) for i in range(num_locs)]
        figsize.append((1.1,0.8))
        figsize_leg = (1.1,0.8)
        
        # Get EF & BiOp rules
        EFrules = get_EFrules()
        EF_rules_list = [EFrules[key] for key in EFrules]
        EF_rules_list = sorted(EF_rules_list, key=lambda x: x[0])  # order list by number
        EF_rules_list = [EF_rules_list[i][1] for i in range(num_locs)]
        
        # Calculate Baseline
        file_nm = res_data_file
        baseline = {}
        for key in SimulatedHistoric:
            data1=[mfx(file_nm[i].replace(file_baseline+'Run0',SimulatedHistoric[key]), column=res_data_EF_col[i], skip=cst.day_of_year_oct1) for i in range(num_locs)]
            num_yrs = np.shape(data1[0])[0]       
            viols1 = [RuleReliability(data1[i],num_yrs, EF_rules_list[i], season='summer') for i in range(num_locs)]  # num of rule violations per year
            baseline.update({key:[np.mean(viols1[i]) for i in range(num_locs)]})  
                
        # Calculate baseline-subtracted value
        data_to_stack = []
        for key in scenarios:
            data1=[mfx(file_nm[i].replace(file_baseline+'Run0',scenarios[key]), column=res_data_EF_col[i], skip=cst.day_of_year_oct1) for i in range(num_locs)]
            num_yrs = np.shape(data1[0])[0]       
            viols1 = [RuleReliability(data1[i],num_yrs, EF_rules_list[i], season='summer') for i in range(num_locs)]  # num of rule violations per year
            data_to_stack.append([np.subtract(movingaverage(viols1[i],window), baseline[scenarios_own[key]][i]) for i in range(num_locs)])  
            if key == baseline_case:
                viols_smthd = [np.subtract(movingaverage(viols1[i],window), baseline[scenarios_own[key]][i]) for i in range(num_locs)]

        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(num_locs)]
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(num_locs)] 
        upper = [np.max(data_stacked[i][8:83],1) for i in range(num_locs)]
        lower = [np.min(data_stacked[i][8:83],1) for i in range(num_locs)]
            
        maxd = np.max(np.array([np.max(upper[i]) for i in range(num_locs)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(num_locs)]))
        viols_smthd = [viols_smthd[i][8:83] for i in range(num_locs)]
        xctr = 0.5
        yctr = 0.75
        
        redblue = ['blue','red']
        num_yrs = len(viols_smthd[0])
        write_tinyfigs2(viols_smthd, upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \, Sum \,Reliab\,$ [days]'
        xlabel = 'Red = less Summer reliability'
        write_legend2(viols_smthd[0], upper[0], lower[0],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5, which_legend = 'EFs')
               
        
        title = "Summer Reliability of BiOp and Env Flows"
        file_graphics = 'change_in_Biop-EF_summer_reliability_wGrphs.png'        
        graphs = range(num_locs+1); graphs.remove(0)

        EFlats_tweaked = EFlats
        EFlats_tweaked[7] = EFlats_tweaked[7] - 0.05
        EFlats_tweaked[6] = EFlats_tweaked[6] - 0.03
        write_map(title, EFlons, EFlats_tweaked, file_graphics, get_metadata(file_nm[0]), 
                  shp, graphs=graphs, lons2=dam_data_lons, lats2=dam_data_lats)
       

##############################################################################
#  ENVIRONMENTAL FLOWS        
############  BiOp & Env Flows w mini figs NOT SUMMER  ############    
    elif plot_num == 103:
        plt.close()
        window = binomial_window(15)
        num_locs = len(res_data_list)
        figsize=[(1.1,0.8) for i in range(num_locs)]
        figsize.append((1.1,0.8))
        figsize_leg = (1.1,0.8)        
        
        # Get EF & BiOp rules
        EFrules = get_EFrules()
        EF_rules_list = [EFrules[key] for key in EFrules]
        EF_rules_list = sorted(EF_rules_list, key=lambda x: x[0])  # order list by number
        EF_rules_list = [EF_rules_list[i][1] for i in range(num_locs)]
        
        # Calculate Baseline
        file_nm = res_data_file
        baseline = {}
        for key in SimulatedHistoric:
            data1=[mfx(file_nm[i].replace(file_baseline+'Run0',SimulatedHistoric[key]), column=res_data_EF_col[i], skip=cst.day_of_year_oct1) for i in range(num_locs)]
            num_yrs = np.shape(data1[0])[0]       
            viols1 = [RuleReliability(data1[i],num_yrs, EF_rules_list[i], season='not_summer') for i in range(num_locs)]  # num of rule violations per year
            baseline.update({key:[np.mean(viols1[i]) for i in range(num_locs)]})  
        
        data_to_stack = []
        for key in scenarios:
            data1=[mfx(file_nm[i].replace(file_baseline+'Run0',scenarios[key]), column=res_data_EF_col[i], skip=cst.day_of_year_oct1) for i in range(num_locs)]
            num_yrs = np.shape(data1[0])[0]       
            viols1 = [RuleReliability(data1[i],num_yrs, EF_rules_list[i], season='not_summer') for i in range(num_locs)]  # num of rule violations per year
            data_to_stack.append([np.subtract(movingaverage(viols1[i],window), baseline[scenarios_own[key]][i]) for i in range(num_locs)])  
            if key == baseline_case:
                viols_smthd = [np.subtract(movingaverage(viols1[i],window), baseline[scenarios_own[key]][i]) for i in range(num_locs)]

        data_to_stack = [tuple([data_to_stack[j][i] for j in range(len(data_to_stack))]) for i in range(num_locs)]
        data_stacked = [np.column_stack(data_to_stack[i]) for i in range(num_locs)] 
        upper = [np.max(data_stacked[i][8:83],1) for i in range(num_locs)]
        lower = [np.min(data_stacked[i][8:83],1) for i in range(num_locs)]
            
        maxd = np.max(np.array([np.max(upper[i]) for i in range(num_locs)]))
        mind = np.min(np.array([np.min(lower[i]) for i in range(num_locs)]))
        viols_smthd = [viols_smthd[i][8:83] for i in range(num_locs)]
        xctr = 0.5
        yctr = 0.75
        
        redblue = ['blue','red']
        num_yrs = len(viols_smthd[0])
        write_tinyfigs2(viols_smthd, upper, lower, figsize,
                        mind,maxd,redblue, num_yrs, facecolor = '0.6',
                        linewidth = 1.5)
        
        ylabel = r'$\Delta \,Reliab\,$ [days]'
        xlabel = 'Red = less Non-Summer reliability'
        write_legend2(viols_smthd[0], upper[0], lower[0],figsize_leg,
                      mind,maxd,redblue,num_yrs,ylabel,xlabel, facecolor='0.6',
                      linewidth=1.5, which_legend = 'EFs')
               
        
        title = "Non-Summer Reliability of BiOp and Env Flows"
        file_graphics = 'change_in_Biop-EF_NONsummer_reliability_wGrphs.png'        
        graphs = range(num_locs+1); graphs.remove(0)

        EFlats_tweaked = EFlats
#        EFlats_tweaked[7] = EFlats_tweaked[7] + 0.03
        EFlats_tweaked[6] = EFlats_tweaked[6] + 0.03
        EFlats_tweaked[3] = EFlats_tweaked[3] + 0.03
        write_map(title, EFlons, EFlats_tweaked, file_graphics, get_metadata(file_nm[0]), 
                  shp, graphs=graphs, lons2=dam_data_lons, lats2=dam_data_lats)

##############################################################################
#  SNOW and PRECIP CORRELATIONS        
############  Correlations of discharge to SWE  ############    

    elif plot_num == 201:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        num_gauge_sig = len(Q_SWE1_sig)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        plt.title("Jul - Aug Discharge & Apr 1 SWE")
        
        import heapq
        data1_2nd_lgst = heapq.nlargest(2, Q_SWE1_sig)[1]  #find second-largest number
        data1_size = np.clip(500.*np.array(Q_SWE1_sig)/data1_2nd_lgst,10.,20000.)
        
        colord = np.array(SWE_frac_sig)
        
        x,y=WBmap(c_Longs_SWE,c_Lats_SWE)
        startcolor = 'blue'
        midcolor1 = 'red'
        endcolor = 'black' #'#4C0000'
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',[startcolor,midcolor1,endcolor],128)
        m = WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1,vmin=0,vmax=1)
        # add colorbar.
        cbar = WBmap.colorbar(m, location = 'bottom', pad='6%', size='3%')#,location='bottom',pad="5%",size='8')
        cbar.set_label('fraction discharge increase with median Apr 1 SWE',size=10)
        cbar.ax.tick_params(labelsize=9) 
        
        file_graphics = 'Q_Apr1SWE_correlations.png'     
        plt.text(0., 0, get_metadata('Q-SWE-PRE.xlsx'), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=400, bbox_inches='tight')
        plt.close()       
        
##############################################################################
#  SNOW and PRECIP CORRELATIONS        
############  Correlations of discharge to PRECIP  ############    

    elif plot_num == 202:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
        
        num_gauge_sig = len(Q_PRE1_sig)
        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        plt.title("Jul - Aug Discharge & Feb - Apr Precip")
        
        import heapq
        data1_2nd_lgst = heapq.nlargest(2, Q_PRE1_sig)[1]  #find second-largest number
        data1_size = np.clip(500.*np.array(Q_PRE1_sig)/data1_2nd_lgst,10.,20000.)
        
        colord = np.array(PRE_frac_sig)
        
        x,y=WBmap(c_Longs_PRE,c_Lats_PRE)
        startcolor = 'blue'
        midcolor1 = 'red'
        endcolor = 'black' #'#4C0000'
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',[startcolor,midcolor1,endcolor],128)
        m = WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1,vmin=0,vmax=1)
        # add colorbar.
        cbar = WBmap.colorbar(m, location = 'bottom', pad='6%', size='3%')#,location='bottom',pad="5%",size='8')
        cbar.set_label('fraction discharge increase with avg Feb - Apr precip',size=10)
        cbar.ax.tick_params(labelsize=9) 
        
        file_graphics = 'Q_Feb-AprPrecip_correlations.png'     
        plt.text(0., 0, get_metadata('Q-SWE-PRE.xlsx'), fontsize=3,
                verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=400, bbox_inches='tight')
        plt.close()       

##############################################################################
#  SNOW and PRECIP CORRELATIONS        
############  Correlations of discharge to PRECIP  ############    

    elif plot_num == 204:
        fig = plt.figure(figsize=(6,8))
        ax2 = fig.add_axes()
        plt.axes(frameon=False)
#        c_Longs_model
#        c_Lats_model
        scenario = file_historical
        file_nm = data_path + 'Discharge_(Subbasins)'+scenario+'Run0.csv'
        file_nm_WBSWE = data_path + 'Snow_(mm)'+scenario+'Run0.csv'
        data1=[mfx(file_nm,column=subbasin_data_order[i],skip=cst.day_of_year_oct1) for i in range(12)]
        data1[7] = data1[7] - data1[8]  # correct N Santiam for S Santiam contribution
        num_yrs = np.shape(data1[0])[0]
        shft = 365 - cst.day_of_year_oct1
        jul1 = cst.day_of_year_jul1 + shft
        aug31 = cst.day_of_year_aug31 + shft
        first_day = jul1
        last_day = aug31
        summer_Q_by_yr = [[nrc(data1[i],[j,first_day],[j,last_day]) for j in range(num_yrs)] for i in range(12)]  # Start of summer = day 260, end = day 350
        data1=mfx(file_nm_WBSWE,column=1,skip=cst.day_of_year_oct1)
        apr1 = cst.day_of_year_apr1 + shft
        Apr1_SWE_by_yr = [nrc(data1,[j,apr1],[j,apr1]) for j in range(num_yrs)] 
        Apr1_SWE_by_yr_norm = np.array(Apr1_SWE_by_yr)/np.median(Apr1_SWE_by_yr)  # normalized SWE to median Apr 1
        regression_stats = [stats.linregress(Apr1_SWE_by_yr_norm,summer_Q_by_yr[i]) for i in range(12)]
        # linregress returns slope, intercept, r-value, p-value, and standard error.  r-square is r-value **2
        Q_SWE1_sig = [regression_stats[i][0]+regression_stats[i][1] for i in range(12)]
        print Q_SWE1_sig
        SWE_frac1 = [regression_stats[i][0]/Q_SWE1_sig[i] for i in range(12)]
        assert False

        
        WBmap=basemap.Basemap(projection='tmerc', llcrnrlat=lat_bounds[0], llcrnrlon=long_bounds[1], 
                    urcrnrlat=lat_bounds[1], urcrnrlon=long_bounds[0], ax=ax2, lon_0=-123., lat_0=(77.+34.4)/2.)
        im = plt.imread('C:\\code\\maplot\\ElevationMap_AdditionalRivers.png')
        WBmap.imshow(im, origin='upper') #interpolation='lanczos', 
        WBmap.readshapefile(shp, 'metadata', drawbounds=True,linewidth=0.25, color='k', )
        plt.title("Jul - Aug Discharge & Feb - Apr Precip Model")
        
        import heapq
        data1_2nd_lgst = heapq.nlargest(2, Q_PRE1_sig)[1]  #find second-largest number
        data1_size = np.clip(500.*np.array(Q_PRE1_sig)/data1_2nd_lgst,10.,20000.)
        
        colord = np.array(PRE_frac_sig)
        
        x,y=WBmap(c_Longs_model,c_Lats_model)
        startcolor = 'blue'
        midcolor1 = 'red'
        endcolor = 'black' #'#4C0000'
        cmap1 = mpl.colors.LinearSegmentedColormap.from_list('my_cmap',[startcolor,midcolor1,endcolor],128)
        m = WBmap.scatter(x, y, marker='o',  s=data1_size, lw=0,c=colord,cmap = cmap1,vmin=0,vmax=1)
        # add colorbar.
        cbar = WBmap.colorbar(m, location = 'bottom', pad='6%', size='3%')#,location='bottom',pad="5%",size='8')
        cbar.set_label('fraction discharge increase with avg Feb - Apr precip',size=10)
        cbar.ax.tick_params(labelsize=9) 
        
        file_graphics = 'Q_Feb-AprPrecip_correlations_model.png'     
        plt.text(0., 0, get_metadata(file_nm), fontsize=3,verticalalignment='top')        
        #plt.show()
        plt.savefig(png_path+file_graphics, format="png", dpi=400, bbox_inches='tight')
        plt.close()      