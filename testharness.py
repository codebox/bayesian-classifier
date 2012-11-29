from __future__ import division
import sys
import os
from classify import Classify
from db import Db

classifier = Classify()

def is_doctype_valid(doctype):
	return Db().get_words_count(doctype) > 0

def check_file(f):
	classifier.validate_file_name(f)
	result = classifier.calculate()
	print result
	return [result]

def check_dir(d):
	results = []
	for f in os.listdir(d):
		if f.endswith(".txt"):
			results += check_file(os.path.join(d,f))

	return results

def show_results(results):
	result_count = len(results)
	print 'Tested with %s document%s' % (result_count, '' if result_count == 1 else 's')
	print 'Result was %1.2f (1 is good, 0 is bad)' % (sum(results) / result_count,)

if __name__ == '__main__':
	usage = 'Usage: %s <file> <expected doctype> <other doctype>' % sys.argv[0]

	if len(sys.argv) != 4:
		raise ValueError(usage)

	input_file = sys.argv[1]
	doctype_expected = sys.argv[2]
	doctype_other = sys.argv[3]

	classifier.validate_doctypes(doctype_expected, doctype_other)

	results = None
	if os.path.isfile(input_file):
		results = check_file(input_file)
	elif os.path.isdir(input_file):	
		results = check_dir(input_file)
	else:
		raise ValueError("Unable to find file/directory '%s'\n%s" % (input_file, usage))

	show_results(results)
