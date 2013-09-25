#!/usr/bin/python3

class deaddropdata(object):

	def __init__(self, block):
		self.block = block
		import sqlite3 as lite
		global con
        # TODO: store the path and name of the database in a config file
        # TODO: check out ConfigParser: http://docs.python.org/2/library/configparser.html
		con = lite.connect('deaddrop.db')
		global cur
		cur = con.cursor()


	def getlastvalues(self):
		#retrieve offset and size of the most recent write
		cur.execute('SELECT MAX(id) FROM files')
		maxid = cur.fetchone()[0]
		cur.execute('SELECT * FROM files WHERE id = (?)',(maxid,))
        # TODO: check for a null or empty result
		values = cur.fetchall()[0]
		(offset, size) = values[1], values[2]
		return (offset, size)


	def findvalues(self, offset):
		#find the size of the file matched to the given offset
		cur.execute('SELECT * FROM files WHERE offset = (?)',(offset,))
        # TODO: check for a null or empty result
		size = cur.fetchall()[0][2]
		return size


	def givevalues(self, offset, size):
		#add the new file's values to the database
        # TODO: validate the offset and size values before inserting into database
        # TODO: (make sure they are integers via test)
		cur.execute('INSERT INTO files(offset, size) VALUES (?,?)',(offset, size))
		con.commit()
