# validate detect config

# imports

import schemas


# functions 

def validate_object(obj, schema):
	'''validates an object in config against the object's schema

	Parameters
	----------
	obj: (dict) object of config
	schema: (dict) schema object in schemas.py

	Returns
	-------
	True if object is validated, otherwise throws error
	'''

	valid_types = set(schema.keys())

	# check that there is only one key
	assert len(obj) == 1

	# check that the data source key is defined in DATA_SOURCE schema
	name = obj.keys()[0]
	assert name in valid_types 

	for k, v in schema[name]['parameters'].items():
		
		param_exists = k in obj[name]

		if param_exists:
			assert isinstance(obj[name][k], v['type'])

		if v['required']:
			assert param_exists

	return True


def validate_config(config):
	'''validates detect config against CONFIG schema in schemas.py
	'''

	# validate config from root level
	validate_object(config, schemas.CONFIG)

	# validate objects in config
	validate_object(config['data'], schemas.DATA_TYPE)
	validate_object(config['detect'], schemas.DETECT_TYPE)
	validate_object(config['notify'], schemas.NOTIFY_TYPE)

	# make sure time and measure col has matching types
	both_strs = isinstance(config['time_col'], str) & isinstance(config['measure_col'], str)
	both_ints = isinstance(config['time_col'], int) & isinstance(config['measure_col'], int)
	assert both_strs or both_ints

	return True
