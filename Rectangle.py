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
    
    data = array_2d[min_y:max_y,min_x:max_x]
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
    else:
        raise BaseException

