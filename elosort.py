#!/usr/bin/env python

import cherrypy
import sqlite3
from optparse import OptionParser
import os
import hashlib
import glob
import random

STARTRANK = 1000

class ELODB:
	def __init__(self, dbfile):
		try:
			open(dbfile)
			self.con = sqlite3.connect(dbfile)
			print "\""+dbfile+"\" found :)"
		except IOError:
			print "\""+dbfile+"\" not found, making a new one"
			self.con = sqlite3.connect(dbfile)
			c = self.con.cursor()
			c.execute('''create table Item
						(hash text PRIMARY_KEY, path text, rank integer)''')
			self.con.commit()
			c.close()

	def filehash(self, filepath):
		f = open(filepath)

		m = hashlib.md5()
		m.update(f.read())

		return m.hexdigest()

	def getrank(self, filepath):
		"""
		Get the ELO rank for a given file.

		If the file isn't already in the db, add it with the starting rank
		"""
		filehash = self.filehash(filepath)

		c = self.con.cursor()
		c.execute('''select rank from Item
						where hash = ?''', (filehash,))

		result = c.fetchone()
		del c

		if result:
			filehash, path, rank = result
			return rank
		else:
			self.initrank(filepath)
			return STARTRANK

	def initrank(self, filepath):
		"""Add a new file to the db, with the starting rank"""
		filehash = self.filehash(filepath)
		abspath = os.path.abspath(filepath)

		c = self.con.cursor()
		c.execute('''insert into Item values (?, ?, ?)''',
					(filehash, abspath, STARTRANK))

		self.con.commit()
		del c


class ELOSort:
	def __init__(self, db, items):
		self.db = db
		self.items = items
		self.itemstack = self.items[:]
		random.shuffle(self.itemstack)

	def index(self, winner=None, loser=None):
		if winner and loser:
			pass

		p1 = self.itemstack.pop()
		p2 = self.itemstack.pop()
		return '''<html><img src="static/%s"><img src="static/%s"></html>''' % (p1, p2)

	index.exposed = True




if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option("--file", dest="file",
					help="EMG trace file name", metavar="FILE")

	(opts, args) = parser.parse_args()

	if args:
		basedir = args[0]
	else:
		basedir = "."


	filename = os.path.join(basedir, ".elosortdb.sql3")

	db = ELODB(filename)

	items = glob.glob(os.path.join(basedir, "*.jpg"))
	random.shuffle(items)

	print items


	conf = {'/static': {'tools.staticdir.on': True,
				'tools.staticdir.dir': os.path.abspath(basedir)
				}
			}

	cherrypy.quickstart(ELOSort(db, items), "/", config=conf)