from __future__ import division
from mode import Mode
from db import Db
from words import text_to_list

class Classify(Mode):
	MIN_WORD_COUNT = 5
	RARE_WORD_PROB = 0.5
	EXCLUSIVE_WORD_PROB = 0.99

	def validate(self, args):
		if len(args) != 5:
			raise ValueError('Usage: %s classify <file> <doctype> <doctype>' % args[0])

		file_contents = None
		try:
			file_contents = open(args[2], 'r').read()
		except Exception as e:
			raise ValueError('Unable to read specified file "%s", the error message was: %s' % (args[2], e))
		
		doctype1 = args[3]
		doctype2 = args[4]

		if doctype1 == doctype2:
			raise ValueError('Please enter two different doctypes')

		d = Db().get_doctype_counts()
		if doctype1 not in d.keys():
			raise ValueError('Unknown doctype: ' + doctype1)

		if doctype2 not in d.keys():
			raise ValueError('Unknown doctype: ' + doctype2)

		self.doctype1 = doctype1
		self.doctype2 = doctype2
		self.words = text_to_list(file_contents)

	def p_for_word(self, db, word):
		total_word_count = self.doctype1_word_count + self.doctype2_word_count

		word_count_doctype1 = db.get_word_count(self.doctype1, word)
		word_count_doctype2 = db.get_word_count(self.doctype2, word)
		
		if word_count_doctype1 + word_count_doctype2 < self.MIN_WORD_COUNT:
			return self.RARE_WORD_PROB

		if word_count_doctype1 == 0:
				return 1 - self.EXCLUSIVE_WORD_PROB
		elif word_count_doctype2 == 0:
				return self.EXCLUSIVE_WORD_PROB

		# P(S|W) = P(W|S) / ( P(W|S) + P(W|H) )

		p_ws = word_count_doctype1 / self.doctype1_word_count
		p_wh = word_count_doctype2 / self.doctype2_word_count

		return p_ws / (p_ws + p_wh)

	def p_from_list(self, l):
		p_product         = reduce(lambda x,y: x*y, l)
		p_inverse_product = reduce(lambda x,y: x*y, map(lambda x: 1-x, l))

		return p_product / (p_product + p_inverse_product)

	
	def execute(self):
		pl = []
		db = Db()

		d = db.get_doctype_counts()
		self.doctype1_count = d.get(self.doctype1)
		self.doctype2_count = d.get(self.doctype2)

		self.doctype1_word_count = db.get_words_count(self.doctype1)
		self.doctype2_word_count = db.get_words_count(self.doctype2)

		for word in self.words:
			p = self.p_for_word(db, word)
			pl.append(p)

		result = self.p_from_list(pl)

		print 'Probability that document is %s rather than %s is %1.2f' % (self.doctype1, self.doctype2, result)
		return result
