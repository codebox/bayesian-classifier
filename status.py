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
		print '''%s
Status:
    Scam Ads:     %s
    Non-Scam Ads: %s
%s''' % (bar, db.get_ad_count(True), db.get_ad_count(False), bar)
