from mode import Mode

class Classify(Mode):
	def name(self):
		return 'classify'

	def validate(self, args):
		if len(args) != 3:
			raise ValueError('Usage: %s classify <file>' % args[0])

		file_contents = None
		try:
			file_contents = open(args[2], 'r').read()
		except Exception as e:
			raise ValueError(usage + '\nUnable to read specified file "%s", the error message was: %s' % (args[2], e))
		
		return lambda f: f(file_contents)

	def execute(self):
		print 'classify'