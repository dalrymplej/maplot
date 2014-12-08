def binomial_window(averaging_window):
    """ return window for binomial filter"""
    import numpy as np
    
    window_raw = np.array([])
    window_raw = np.append(window_raw,[n_take_k(averaging_window-1,i) for i in range(averaging_window)])
    window = window_raw / np.sum(window_raw)  # normalized weights
    return window


def n_take_k(n,k):
    """Returns (n take k),
    the binomial coefficient.

    author: https://code.google.com/p/econpy/source/browse/trunk/pytrix/pytrix.py
    """
    n, k = int(n), int(k)
    assert (0<=k<=n), "n=%f, k=%f"%(n,k)
    k = min(k,n-k)
    c = 1
    if k>0:
        for i in xrange(k):
            c *= n-i
            c //= i+1
    return c

def movingaverage(interval, window):
    """
    Calculate a moving average and return numpy array (dimension 1)
    """
    import numpy as np
    return np.convolve(interval, window, 'same')

def movingaverage_first2D(array_2D, window_size_days, window_size_yrs):
    """
    Calculate a moving average of first window_size_yrs years over
      a window of window_size_days, and return a numpy array (dimension 1)
    """
    import numpy as np
    interval = [np.average(array_2D[0:window_size_yrs,i]) for i in range(365)]
    window = np.ones(int(window_size_days))/float(window_size_days)
    return np.convolve(interval, window, 'same')

def movingaverage_2D(array_2D, window_size_days):
    """
    Take a np array and calculate a moving average over a window of 
    window_size_days, and return a numpy array (dimension 2)
    """
    import numpy as np
    from matrix_from_xls import data_2D
    data = array_2D.flatten()
    window = np.ones(int(window_size_days))/float(window_size_days)
    data = np.convolve(data, window, 'same')
    return data_2D(data,0,365)
    
