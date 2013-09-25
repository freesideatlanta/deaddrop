#!/usr/bin/python3

class deaddropdata(object):

	def __init__(self, block):
		self.block = block
		import sqlite3 as lite
		global con
		con = lite.connect('deaddrop.db')
		global cur
		cur = con.cursor()


	def getlastvalues(self):
		#retrieve offset and size of the most recent write
		cur.execute('SELECT MAX(id) FROM files')
		maxid = cur.fetchone()[0]
		cur.execute('SELECT * FROM files WHERE id = (?)',(maxid,))
		values = cur.fetchall()[0]
		(offset, size) = values[1], values[2]
		return (offset, size)


	def findvalues(self, offset):
		#find the size of the file matched to the given offset
		cur.execute('SELECT * FROM files WHERE offset = (?)',(offset,))
		size = cur.fetchall()[0][2]
		return size


	def givevalues(self, offset, size):
		#add the new file's values to the database
		cur.execute('INSERT INTO files(offset, size) VALUES (?,?)',(offset, size))
		con.commit()
