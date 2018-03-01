# code to process a config

# 1) validate
# 2) load data
# 3) process data with detect type
# 4) generate notify output
# 5) create visualization

#------------------------------------------------------------------------------
# imports

import yaml

from configs import read, schemas, validate


#------------------------------------------------------------------------------
# functions

def read_config(fp):
	''' read in config
	'''

	with open(fp, 'r') as f:
		config = yaml.load(f)
	return config


def add_obj_defaults(obj, schema):
	'''adds in default parameter values if not specified in config object
	'''	
	
	obj_type  = obj.keys()[0]
	for k, v in schema[obj_type]['parameters'].items():
		if not v['required']:
			if k not in obj:
				obj[k] = v['default']
	return obj


# TODO: Cleanup by looping through required/not required keys 
def preprocess_config(config):
	'''validate and add defaults
	'''

	validate.validate_config(config)
	
	# add defaults for root keys and objects
	config['detect'] = add_obj_defaults(config['detect'], schemas.DETECT_TYPE)
	config['data'] = add_obj_defaults(config['data'], schemas.DATA_TYPE)

	if 'look_back' not in config:
		config['look_back'] = schemas.CONFIG['look_back']['default']

	if 'notify' in config:
		config['notify'] = add_obj_defaults(config['notify'], schemas.NOTIFY_TYPE)

	return config


def read_data(data_obj):
    '''load data as how and from as specified in the config
    '''
    
    name = data_obj.keys()[0]
    print data_obj[name]['fp']
    if name == 'csv':
        fp = data_obj[name]['fp']
        data = read.csv(fp)
        
    if name == 's3':
        print 'Whoops, not available yet, ya dingus!'

    if name == 'sql':
        print 'Whoops, not available yet, ya dingus!'
        
    return data




