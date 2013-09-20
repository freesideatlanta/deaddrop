#!/usr/bin/python3
# Filename: deaddrop.py

import sqlite3 as lite

con = lite.connect('deaddrop.db')
cur = con.cursor()
block = 'block'

def getvalues():
	#retrieve offset and size of the most recent write
	cur.execute('SELECT MAX(id) FROM files')
	maxid = cur.fetchone()[0]
	cur.execute('SELECT * FROM files WHERE id = (?)',(maxid,))
	values = cur.fetchall()[0]
	(offset, size) = values[1], values[2]
	return (offset, size)

def findvalues(offset):
	#find the size of the file matched to the offset given
	cur.execute('SELECT * FROM files WHERE offset = (?)',(offset,))
	size = cur.fetchall()[0][2]
	return size
	
def givevalues(offset, size):
	#add the new file to the database
	cur.execute('INSERT INTO files(offset, size) VALUES (?,?)',(offset, size))
	con.commit()

def getsize(filename):
	#finds the size of a file
	s = open(filename, 'r+b')
	s.seek(0,2)
	bytesize = s.tell()
	return bytesize
	s.close()

def writefile(filename, offset):
	#writes a file to the block
	e = open(block, 'r+b')
	f = open(filename, 'r+b')
	e.seek(offset)
	e.write(f.read())
	size = getsize(filename)
	f.close()
	e.close()

def retrievefile(filename, offset, size):
	#retrieves a file from the block
	e = open(block, 'r+b')
	f = open(filename, 'w+b')
	e.seek(offset)
	f.write(e.read(size))
	f.close()
	e.close()
	
while True:

	action = input(
	'''What would you like to do?\n
	(w)rite a file to the block\n
	(r)etrieve a file from the block\n
	(q)uit\n> ''')

	if action == 'w':
		filename = input('What is the name of the file you want to write? ')
		offset = getvalues()[0] + getvalues()[1]
		writefile(filename, offset)	
		givevalues(offset, getsize(filename))
		print('The offset is ' + str(offset))

	elif action == 'r':
		filename = input('What should the retrieved file be called? ')
		offset = int(input('What is the offset of the file? '))
		size = findvalues(offset)
		retrievefile(filename, offset, size)

	elif action == 'q':
		break

	else:
		print('That is not a valid command')
print('Done')
