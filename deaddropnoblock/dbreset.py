#!/usr/bin/python3
#Careful. This will reset the database

import sqlite3 as lite

con = lite.connect('deaddrop.db')
cur = con.cursor()

with con:
	cur.executescript('''
		DROP TABLE IF EXISTS files;
		CREATE TABLE files(id INTEGER PRIMARY KEY, offset INT, size INT);
		INSERT INTO files(offset, size) VALUES (0,1);
		''')
print('Database Reset')
