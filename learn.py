from mode import Mode

class Learn(Mode):
	def name(self):
		return 'learn'

	def validate(self, args):
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

			self.file_contents = file_contents
			self.count = count
			self.is_scam = learn_type == scam_type

		else:
			raise ValueError(usage)				

	def execute(self):
		print 'learn'