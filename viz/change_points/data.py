# create moving average timeseries for window widths 12, 24, 36, 48, 60  

import json

import numpy as np
import pandas as pd
	

def make_data(ts, windows):
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


def save_data(data):
	'''saves data to data dir as json object
	'''

	with open('data/change_points_data.json', 'w') as f:
	    json.dump(data, f)


if __name__ == '__main__':
	# make fake data
	ts = pd.Series(np.random.normal(0, 1, 300))
	freq = 'H'
	times = pd.date_range('2018-01-01', periods=ts.shape[0], freq=freq) 
	ts.index = pd.DatetimeIndex(times)
	windows = np.arange(1, 20 + 1) * 6
	save_data(
		make_data(ts, windows))


