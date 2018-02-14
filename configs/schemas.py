from openmail_common import 


DATA = {

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
		},
	}
}


DETECT_TYPES = {
	
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












