#Created by Owen Haggerty on the 16th of November, 2014
import numpy as np

def np_rec_calc(array_2d,bottom_left,top_right,oper='avg'):
    '''This function takes a numpy array and coordinates in the array and outputs
    the rectangular set of data after handling it as specified by oper.

    array_2d: the numpy array
    bottom_left: (list) the lower left coordinate of the desired rectangle
    top_right: (list) the upper right coordinate of the desired rectangle
    oper: (str) a string telling the function how to handle the rectangle
        after it is generated
    
    returns a float
    '''
    max_x = top_right[1]
    min_x = bottom_left[1]
    max_y = top_right[0]
    min_y = bottom_left[0]
    
    data = array_2d[min_y:max_y+1,min_x:max_x+1]
    if oper == 'sum' or oper == 'Sum':
        return np.sum(data)
    elif oper == 'max' or oper == 'Max' or oper == 'maximum' or oper == 'Maximum':
        return np.amax(data)
    elif oper == 'min' or oper == 'Min' or oper == 'minimum' or oper == 'Minimum':
        return np.amin(data)
    elif oper == 'avg' or oper == 'Avg' or oper == 'average' or oper == 'Average':
        return np.average(data)
    elif oper == 'avgmax' or oper == 'AvgMax' or oper == 'averagemaximum' or oper == 'Average_Maximum' or oper == 'AverageMaximum' or oper == 'AverageMax':
        return np.average(np.amax(data,1))  # max of each row then average those
    elif oper == 'avgmin' or oper == 'AvgMin' or oper == 'averageminimum' or oper == 'Average_Minimum' or oper == 'AverageMinimum' or oper == 'AverageMin':
        return np.average(np.amin(data,1)) # min of each row then average those
    elif oper == 'stdev' or oper == 'Deviation' or oper == 'deviation' or oper == 'standard_deviation':
        return np.std(data)
    elif oper == 'median' or oper == 'Median' or oper == 'Med' or oper == 'med':
        return np.median(data)
    elif oper == '5%' or oper == 'five%' or oper == '5percentile' or oper == 'fifthpercentile':
        return np.percentile(data,5)
    elif oper == '10%' or oper == 'ten%' or oper == '10percentile' or oper == 'tenthpercentile':
        return np.percentile(data,10)
    elif oper == '25%' or oper == 'twentyfive%' or oper == '25percentile' or oper == 'twentyfifthpercentile':
        return np.percentile(data,25)
    elif oper == '75%' or oper == 'seventyfive%' or oper == '75percentile' or oper == 'seventyfifthpercentile':
        return np.percentile(data,75)
    elif oper == '90%' or oper == 'ninety%' or oper == '90percentile' or oper == 'ninetiethpercentile':
        return np.percentile(data,90)
    elif oper == '95%' or oper == 'ninetyfive%' or oper == '95percentile' or oper == 'ninetyfifthpercentile':
        return np.percentile(data,95)
    else:
        raise BaseException

