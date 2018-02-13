import numpy as np
import pandas as pd


def threshold(ts, bound, where='below'):
    '''detect when a threshold is crossed above or below
    
    Parameters
    ----------
    ts         : Pandas Series or DataFrame with datetime index
    bound      : threshold value to compare values of the timeseries against
                 and mark when the values are above and/or below the threshold.
                 If a length 2 list or tuple is passed, then defaults to checking 
                 if values are below `bound[0]` and above `bound[1]`. Otherwise, compares
                 above or below based on `when` parameter.
    where      : values allowed are `below`, `above`, `both`. If `below`, then check where
                 values of `ts` are below `bound`, and if `above` then check where values of
                 `ts` are above `bound`. Defaults to `below`.
           
    Returns
    -------
    A DataFrame with matching index to input `ts` with two boolean columns, `below` and `above`,
    which index values below and above input threshold bound, respectively.
    '''
    
    if isinstance(bound, (tuple, list)):
        # TODO: add error handling for if input is not length 2
        # Should probably create a tuple (b, inf) or (-inf, b)
        lower, upper = tuple(bound)
    else:
        if where == 'below':
            lower, upper = bound, np.inf
        elif where == 'above':
            lower, upper = -np.inf, bound
    return ts < lower, ts > upper


def trend_seq_label(x, step):
    '''
    '''
    
    if isinstance(step, (list, tuple)):
        down, up = tuple(step)
    else:
        down, up = -step, step
    
    if x < down:
        res = 'down'
    elif x > up:
        res = 'up'
    else:
        res = 'flat'
    return res


def trend_seq(ts, step=0):
    '''converts a timeseries into a sequence of trend designations `down`, `flat`, `up`
    
    Parameters
    ----------
    ts
    step:
    '''
    
    deltas = ts - ts.shift(1)
    return deltas.apply(trend_seq_label, args=(step,))


def contiguous_cumcount(x):
    '''computes cumulative counts for contiguous equal records
    '''
    
    return x.groupby((x != x.shift(1)).cumsum()).cumcount() + 1


def trend_runs(ts, step=0, signed=False):
    '''computes cumultive run length for trend sequence labels
    '''
    
    seq = trend_seq(ts, step=step)
    runs = contiguous_cumcount(seq)
    if signed:
        sign_map = {'up': 1, 'flat': 0, 'down': -1}
        runs = seq.replace(sign_map) * runs
    return runs


def variance_band(ts, radius=1, method='stdev', window=None, auto_window=True):
    '''computes a threshold timeseries based on variance of previous window
    
    Parameters
    ----------
    ts:
    radius:
    method: One of 
        stdev   - standard deviation 
        mad     - mean absolute deviation
        var     - variance
        pearson - Pearson's index of skewness
    window: (int) postive integer >= 3. Size of window to compute method over.
    auto_window: (bool) Use window as 1/5 of number of rows of ts. Defaults to True
    '''
    
    assert method in set(['stdev', 'mad', 'var', 'pearson'])    
    assert (isinstance(window, int) and window >= 3) or (window is None)
    
    if auto_window and window is None:
        window = int(np.floor(ts.shape[0] * 0.2))
        
    if method == 'stdev':
        variances = ts.rolling(window).std()
    elif method == 'mad':
        variances = ts.rolling(window).apply(mad)
    elif method == 'var':
        variances = ts.rolling(window).var()
    elif method == 'pearson':
        variances = ts.rolling(window).apply(pearson)
    return variances


def ma_change_points(ts, window=None, auto_window=True):
    '''
    '''
        
    if auto_window and window is None:
        window = (
            int(np.floor(ts.shape[0] * 0.1)),
            int(np.floor(ts.shape[0] * 0.5))
        )
    w1, w2 = window
    ma1, ma2 = ts.rolling(w1).mean(), ts.rolling(w2).mean()
    return ma1, ma2, ma1 < ma2        
    
        
def mad(col):
    '''computes mean absolute deviation
    '''
    
    return abs(col - col.mean()).sum()


def pearson(col):
    '''computes Pearson's index of skewness
    '''    
    
    return (3 * (col.mean() - np.median(col))) / col.std()