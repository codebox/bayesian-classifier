class Mode:
	def validate(self):
		raise NotImplementedError()

	def execute(self):
		raise NotImplementedError()

	def name(self):
		raise NotImplementedError()
