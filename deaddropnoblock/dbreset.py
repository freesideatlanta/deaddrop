#!/usr/bin/python3
#Careful. This will reset the database

import sqlite3 as lite
import configparser

config = configparser.ConfigParser()
config.read('deaddrop.ini')

database = config['Options']['Database']

con = lite.connect(database)
cur = con.cursor()

with con:
	cur.executescript('''
		DROP TABLE IF EXISTS files;
		CREATE TABLE files(id INTEGER PRIMARY KEY, offset INT, size INT);
		INSERT INTO files(offset, size) VALUES (0,1);
		''')
print('Database Reset')
