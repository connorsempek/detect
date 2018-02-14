import numpy as np
import pandas as pd


def threshold(ts, lower=None, upper=None):
    '''detect when a threshold is crossed above or below
    
    Parameters
    ----------
    ts         : Pandas Series or DataFrame with datetime index
    lower      : lower threshold value
    upper      : upper threshold value
           
    Returns
    -------
    A tuple of boolean series low, high, and mid where low contains all points
    in ts whose values are < lower, high contains all points in ts whose 
    values are > upper and mid contains all points in ts whose values are
    between lower and upper inclusive. All have the same datetime index as the
    input series.
    '''
    
    if lower is None:
        lower = -np.inf

    if upper is None:
        upper = np.inf

    return ts < lower, ts > upper, (ts >= lower) & (ts <= upper) 


def threshold_alert(ts, lower, upper, between=False, look_back=1):
    '''determine if threshold criteria warrant alerting
    '''
    
    low, high, mid = threshold(ts, lower=LOWER, upper=UPPER)

    # check if values in lookback period warrant alerts
    alert_low = low.iloc[-look_back:].sum() > 0
    alert_high = high.iloc[-look_back:].sum() > 0
    alert_mid = mid.iloc[-look_back:].sum() > 0

    return alert_low, alert_high, alert_mid


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