
from mode import modes

def validate_reset(args):
	if len(args) != 2:
		raise ValueError('Usage: %s reset' % args[0])
	return lambda f: f()

def validate_classify(args):
	if len(args) != 3:
		raise ValueError('Usage: %s classify <file>' % args[0])

	file_contents = None
	try:
		file_contents = open(args[2], 'r').read()
	except Exception as e:
		raise ValueError(usage + '\nUnable to read specified file "%s", the error message was: %s' % (args[2], e))
	
	return lambda f: f(file_contents)

def validate_learn(args):
	scam_type = 'scam'
	non_scam_type = 'nonscam'
	valid_args = False
	usage = 'Usage: %s learn %s|%s <file> <count>' % (args[0], scam_type, non_scam_type)

	if len(args) == 5:
		learn_type = args[2]
		if learn_type not in [scam_type, non_scam_type]:
			raise ValueError(usage + '\nInvalid document type argument, expected "%s" or "%s"' % (scam_type, non_scam_type))
		
		file_contents = None
		try:
			file_contents = open(args[3], 'r').read()
		except Exception as e:
			raise ValueError(usage + '\nUnable to read specified file "%s", the error message was: %s' % (args[3], e))

		count = 0
		try:
			count = int(args[4])
		except:
			raise ValueError(usage + '\nEnter an integer value for the "count" parameter')			

		return lambda f: f(file_contents, count, learn_type == 'scam')	

	else:
		raise ValueError(usage)			
	

def validate(args):
	usage = 'Usage: %s %s <mode specific args>' % (args[0], '|'.join(modes.keys()))
	if (len(args) >= 2):
		mode = args[1]
		if mode in modes:
			return [mode, modes[mode](args)]

		else:
			raise ValueError(usage + '\nUnrecognised mode: ' + args[1])

	else:
		raise ValueError(usage)


