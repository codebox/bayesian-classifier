from db import Db
from mode import Mode

class Status(Mode):
	def name(self):
		return 'status'

	def validate(self, args):
		if len(args) != 2:
			raise ValueError('Usage: %s status' % args[0])

	def execute(self):
		db = Db()
		bar = '=' * 40
		print 'Status:\n'
		for doctype, count in db.get_doctype_counts().items():
			print doctype, ': ', count

