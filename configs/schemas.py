# detect config schema definitions

DATA_SOURCE = {

	'csv': {
		'parameters': {
			'fp': {'type': [str]}
		}
	},

	's3': {
		'parameters': {
			'url': {'type': [str]}
		}
	},

	'query': {
		'parameters': {
			'sql': {'type': [str]},
			'db': {'type':[str]},
		}
	}
}


DETECT_TYPE = {
	
	# ********** THRESHOLD **********
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

# TODO: need to create message bodies to populate slack and email notifications
NOTIFY_TYPE = {
	
	'email': {
		'parameters': {
			'recipients': {'type': list, 'required': True},
		}
	}
	# TODO: Add slack bot alerting
	'slack': {
		'parameters': {
			'channel': {'type': str, 'required': True},
			'name': {'type': str, 'required': True}
		}
	}
}


CONFIG = {

	'name': {'type': [str], 'required': True},
	'detect_type': {'type': [dict], 'required': True},
	'data': {
		'source': {'type': [dict], 'required': True},
		'time_col': {'type': [str], 'required': True},
		'metric_col': {'type': [str],'required': True},
		'required': True
	},
	'look_back': {
		'type':[int], 
		'default': 1,
		'required': False
	}
	'notify': {'type': [dict], 'required': True}
}

