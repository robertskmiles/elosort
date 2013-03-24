#!/usr/bin/env python

import cherrypy
import sqlite3
from optparse import OptionParser
import os
import hashlib


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
		filehash = self.filehash(filepath)
		abspath = os.path.abspath(filepath)

		c = self.con.cursor()
		c.execute('''insert into Item values (?, ?, ?)''',
					(filehash, abspath, STARTRANK))

		self.con.commit()
		del c


class ELOSort:
	def __init__(self, db):
		self.db = db

	def index(self, winner=None, loser=None):
		if winner and loser:
			pass

			

			if sort_by != '':
				results.sort(key=attrgetter(sort_by), reverse=sort_reverse)

		return """<html><b>%s</b> beat <b>%s</b></html>""" % (winner, loser)

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
	print db.con
	print db.getrank(opts.file)

	#cherrypy.quickstart(ELOSort(db))