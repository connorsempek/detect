# create moving average timeseries for window widths 12, 24, 36, 48, 60  

import itertools
import json

import numpy as np
import pandas as pd
	

def make_rolling_means(ts, windows):
	'''
	'''

	mas = []
	for w in windows:
	    ma = ts.rolling(window=w).mean().reset_index()
	    ma['window'] = w
	    mas.append(ma)
	mas = pd.concat(mas)
	mas.columns = ['hr', 'ma', 'window']
	mas = mas[mas['ma'].notnull()]

	mas['hr'] = mas['hr'].dt.strftime('%Y-%m-%d %H:%M:%S')
	mas['ma'] = mas['ma'].round(2)

	ma1, ma2 = mas.copy(), mas.copy()
	ma1['ma_id'] = 1
	ma2['ma_id'] = 2
	mas = pd.concat([ma1, ma2])

	return [row.to_dict() for _, row in mas.iterrows()]


def make_change_points(ts, windows):
	'''
	'''

	mas = []
	for w in windows:
	    ma = ts.rolling(window=w).mean().reset_index()
	    ma['window'] = w
	    ma.columns = ['hr', 'ma', 'window']
	    mas.append(ma)
	pairs = itertools.product(*[mas, mas])
	mas = pd.concat([pd.merge(*pair, on=['hr'], suffixes=('_1', '_2')) for pair in pairs])
	x = (mas['ma_1'] < mas['ma_2']).cumsum()
	cps = mas[(x - x.shift(1)).fillna(0) > 0]
	cps = pd.merge(
	    cps.set_index('hr'),
	    pd.DataFrame(ts, columns=['val']),
	    left_index=True,
	    right_index=True,
	    how='inner'
	).reset_index()
	cps.rename(columns={'index':'hr'}, inplace=True)
	cps['hr'] = cps['hr'].dt.strftime('%Y-%m-%d %H:%M:%S')
	print cps.head()
	return [row.to_dict() for _, row in cps.iterrows()]


def save_data(mas, cps):
	'''saves data to data dir as json object
	'''

	with open('data/rolling_means_data.json', 'w') as f:
	    json.dump(mas, f)

   	with open('data/change_points_data.json', 'w') as f:
	    json.dump(cps, f)


if __name__ == '__main__':

	# make example data
	ts = pd.Series(np.random.normal(0, 1, 300))
	freq = 'H'
	times = pd.date_range('2018-01-01', periods=ts.shape[0], freq=freq) 
	ts.index = pd.DatetimeIndex(times)
	windows = np.arange(1, 20 + 1) * 6

	mas = make_rolling_means(ts, windows)
	cps = make_change_points(ts, windows)
	save_data(mas, cps)

