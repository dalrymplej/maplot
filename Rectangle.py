#Created by Owen Haggerty on the 16th of November,2014
import numpy as np

def np_rec_calc(array_2d,bottom_left,top_right,oper='avg'):
    '''
This function takes a numpy array and coordinates in the array and outputs
the rectangular set of data after handling it as specified by oper.

array_2d: the numpy array
bottom_left: the lower left coordinate of the desired rectangle
top_right: the upper right coordinate of the desired rectangle
oper: a string telling the function how to handle the rectangle
after it is generated
    '''
    max_x = top_right[0]
    min_x = bottom_left[0]
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
    else:
        raise BaseException

x = range(64)
x = np.reshape(x,[8,8])
print np_rec_calc(x,[2,2],[6,6])
