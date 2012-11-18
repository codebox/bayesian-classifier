from mode import Mode
from status import Status
from db import Db

class Reset(Mode):
	def name(self):
		return 'reset'

	def validate(self, args):
		if len(args) != 2:
			raise ValueError('Usage: %s reset' % args[0])

	def execute(self):
		Db().reset()
		print 'Reset Complete'
		Status().execute()
