import sys
import re
import sqlite3
import getopt
import codecs
from collections import defaultdict
from learn import Learn
from classify import Classify
from reset import Reset
from status import Status
from db import Db

'''
create table ok_words(word, count);
create table scam_words(word, count);
create table ad_counts(is_scam, count);
insert into ad_counts (is_scam, count) values (1, 0);
insert into ad_counts (is_scam, count) values (0, 0);

create index i1 on ok_words(word);
create index i2 on scam_words(word);

P(W|L) = P(L|W) . P(W) / P(L)


delete from ok_words;
delete from scam_words;
update ad_counts set count = 0;

'''
commonWords = ('the','be','to','of','and','a','in','that','have','it','is','im','are','was','for','on','with','he','as','you','do','at','this','but','his','by','from','they','we','say','her','she','or','an','will','my','one','all','would','there','their','what','so','up','out','if','about','who','get','which','go','me','when','make','can','like','time','just','him','know','take','person','into','year','your','some','could','them','see','other','than','then','now','look','only','come','its','over','think','also','back','after','use','two','how','our','way','even','because','any','these','us')
'''
def cleanUpWord(word):
	word = re.sub('\W', '', word.lower())
	if (len(word) < 2):
		return None
	elif (word.isdigit()):
		return None
	elif (word in commonWords):
		return None
	
	return word


def update_db_with_dict(d, ad_count, is_scam_data):
	db = Db()
	db.update_ad_count(ad_count, is_scam_data)
	db.update_word_counts(d, is_scam_data)

def add_words_to_dict(l, d):
	for word in l:
		d[word] += 1

def ad_to_word_list(ad_text):
	cleaned_words = map(cleanUpWord, ad_text.split(' '))
	return filter(lambda word : word and (len(word) > 0), cleaned_words)

def file_to_ad_list(file_name):
	return codecs.open(file_name, 'r', 'utf-8').read().split('\n')

def process_file(file, is_scam_data):
	print 'Processing ', file
	ad_list = file_to_ad_list(file)
	ad_count = len(ad_list)
	print 'Found ',ad_count,'adverts in file - building dictionary...'
	d = defaultdict(int)
	i=1
	for ad_text in ad_list:
		word_list = ad_to_word_list(ad_text)
		add_words_to_dict(word_list, d)
		i += 1
		if i % 10000 == 0:
			print 'Processed ',i
		if i > 100000:
			break

	update_db_with_dict(d, ad_count, is_scam_data)

def learn(non_scam_file, scam_file):
	process_file(non_scam_file, False)
	process_file(scam_file, True)

def calc_p_word(word):
	pass

def calc_p_words(p_word_list):
	pass

def get_total_word_count(c, for_scams):
	pass

def classify(input_file):
	text = open(input_file).read()
	words = ad_to_word_list(text)

	conn = sqlite3.connect('./scam.db')
	c = conn.cursor()
	scam_word_count = get_ad_count(c, True)
	ok_word_count = get_ad_count(c, False)


	p_word_list = []
	for word in words:
		p_word_list.append(calc_p_word(word))

	return calc_p_words(p_word_list)

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print 'Usage: %s <input file>' % sys.argv[0]
		
	else:
		input_file = sys.argv[1]
		classify(input_file)
			
'''

modes = {}

def register_mode(mode_class):
	modes[mode_class.__name__.lower()] = mode_class

if __name__ == '__main__':
	register_mode(Learn)
	register_mode(Classify)
	register_mode(Reset)
	register_mode(Status)

	args = sys.argv
	usage = 'Usage: %s %s <mode specific args>' % (args[0], '|'.join(modes.keys()))

	try:
		if (len(args) < 2):
			raise ValueError(usage)

		mode_name = args[1]
		if mode_name not in modes:
			raise ValueError(usage + '\nUnrecognised mode: ' + mode_name)

		mode = modes[mode_name]()
		mode.validate(args)
		mode.execute()

	except Exception as e:
		print e
