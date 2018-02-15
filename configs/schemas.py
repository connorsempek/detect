# detect config schema definitions

DATA_TYPE = {

	'csv': {
		'parameters': {
			'fp': {'type': [str], 'required':True}
		}
	},

	's3': {
		'parameters': {
			'url': {'type': [str], 'required':True}
		}
	},

	'query': {
		'parameters': {
			'sql': {'type': [str], 'required':True},
			'db': {'type':[str], 'required':True},
		}
	}
}


DETECT_TYPE = {
	
	'threshold': {
		'parameters': {

			'lower': {
				'type': [float, int],
				'required': False,
				'default': None
			},
		
			'upper': {
				'type': [float, int],
				'required': False,
				'default': None
			},

			'between': {
				'type': [bool],
				'required': False,
				'default': False
			},
			
			'look_back': {
				'type': [int],
				'required': False,
				'default': 1
			}
		}
	}
}

# TODO: add functionality to support these types :)
NOTIFY_TYPE = {
	
	'email': {
		'parameters': {
			'recipients': {'type': list, 'required': True},
		}
	}
	'slack': {
		'parameters': {
			'channel': {'type': str, 'required': True},
			'name': {'type': str, 'required': True}
		}
	}
	'jira': {
		'parameters': {
			'key': {'type': str, 'required': True},
			'user': {'type': str, 'required': True}
		}
	}
}


CONFIG = {
	'name': {'type': [str], 'required': True},
	'detect': {'type': [dict], 'required': True},
	'data': {'type': [dict], 'required': True},

	# should move time_col and measure_col to DATA_TYPE schema
	'time_col': {'type': [str], 'required': True},
	'measure_col': {'type': [str], 'required': True},
	
	'look_back': {'type':[int], 'default': 1, 'required': False},
	'notify': {'type': [dict], 'required': True}
}

