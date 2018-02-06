import json

import numpy as np
import pandas as pd


def df_to_vega_json(df):

	return [row.to_dict() for _, row in df.iterrows()]


def series_to_vega_json(df, cols=None):

	if cols is None:
		cols = ['timestamp', 'val']
	return [{k:v for k, v in zip(cols, obs)} for obs in ts.items()]


def save_data(data):
	'''saves data to data dir as json object
	'''

	with open('data/thresholds_data.json', 'w') as f:
	    json.dump(data, f)


ts = pd.Series(np.random.normal(0, 1, 300))
freq = 'H'
times = pd.date_range('2018-01-01', periods=ts.shape[0], freq=freq) 
ts.index = pd.DatetimeIndex(times)
ts.index = map(lambda date: date.strftime('%Y-%m-%d %H:%M:%S'), ts.index)

##################################
# --- do any processing here --- #
##################################

data = series_to_vega_json(ts)
save_data(data)