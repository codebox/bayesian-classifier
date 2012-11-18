import sqlite3

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

class Db:
	def __init__(self):
		self.conn = sqlite3.connect('./scam.db')

	def reset(self):
		c = self.conn.cursor()
		try:
			c.execute('delete from ok_words')
			c.execute('delete from scam_words')
			c.execute('update ad_counts set count = 0')

		finally:
			c.close()
			self.conn.commit()

	def get_table_name(self, is_scam):
		if is_scam:
			return 'scam_words'
		else:
			return 'ok_words'

	def update_word_count(self, c, word, num_to_add_to_count, table_name):
		c.execute('select count from ' + table_name + ' where word=?', (word,))
		r = c.fetchone()
		if r:
			c.execute('update ' + table_name + ' set count=? where word=?', (r[0] + num_to_add_to_count, word))
		else:
			c.execute('insert into ' + table_name + ' (count, word) values (?,?)', (num_to_add_to_count, word))

	def update_word_counts(self, d, is_scam):
		table_name = self.get_table_name(is_scam)
		c = self.conn.cursor()
		try:
			for word, count in d.items():
				self.update_word_count(c, word, count, table_name)
		finally:
			c.close()
			self.conn.commit()

	def get_ad_count(self, is_scam):
		c = self.conn.cursor()
		try:
			c.execute('select count from ad_counts where is_scam=?', (is_scam,))
			return c.fetchone()[0]
		finally:
			c.close()
			self.conn.commit()
		
	def get_word_count(self, word, is_scam):
		table_name = self.get_table_name(is_scam)
		c = self.conn.cursor()
		try:
			c.execute('select count from ' + table_name + ' where word=?', (word,))
			r = c.fetchone()
			if r:
				return r[0]
			else:
				return 0

		finally:
			c.close()
			self.conn.commit()

	def update_ad_count(self, num_new_ads, is_scam_data):
		c = self.conn.cursor()
		try:
			current_count = self.get_ad_count(is_scam_data)
			c.execute('update ad_counts set count=? where is_scam=?', (current_count + num_new_ads, is_scam_data))
				
		finally:
			c.close()
			self.conn.commit()

