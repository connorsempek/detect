# c

import argparse
import os

import pandas as pd
import yaml

from configs import read, schemas, validate
import detect
import process


def make_timeseries(config, data):
	'''create timeseries from data based on config specifications
	'''

	# create time series object
	time_col, meas_col = config['time_col'], config['measure_col']
	ts = data.loc[:, [time_col, meas_col]]
	ts.set_index(pd.DatetimeIndex(ts[time_col]), inplace=True)
	ts.drop(time_col, axis=1, inplace=True)
	return ts


def detect_results(config, ts, alert=False):
	'''run detect method against timeseries data
	'''

	detect_type = config['detect'].keys()[0]
	if alert:
		func = getattr(detect, detect_type + '_alert')
	else:
		func = getattr(detect, detect_type)
	kwargs = config['detect'][detect_type]
	kwargs = {k: v for k, v in kwargs.items() 
		if k in detect_func.__code__.co_varnames}
	return func(ts, **kwargs)


def get_results(name):
	'''
	'''

	# load config
	config_fp = 'alerts/{name}/{name}.yaml'.format(name=name)
	config = process.read_config(config_fp)

	# validate, fill out defaults and process config
	config = process.preprocess_config(config)

	# read in data specified in config, then convert to timeseries
	data = process.read_data(config)
	ts = make_timeseries(config, data)

	detect_res = detect_res(config, ts, alert=False)
	alert_res = detect_res(config, ts, alert=True)

	return detect_res, alert_res


def setup_args():
	'''
	'''

	parser = argparse.ArgumentParser()
	parser.add_argument('n', '--name', type=str)
	args = parser.parse_args()
	return args


if __name__ == '__main__':

	args = setup_args()
	detect_res, alert_res = get_results(args.name)

