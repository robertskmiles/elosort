#!/usr/bin/env python

import cherrypy
import sqlite3
from optparse import OptionParser
import os
import hashlib


class ELODB:
	def __init__(self, dbfile):
		try:
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

	def getrank(self, filepath):
		f = open(filepath)

		m = hashlib.sha512()
		m.update(f.read())
		filehash = m.hexdigest()

		c = self.con.cursor()
		with c:
			c.execute('''select rank from Item
						where hash = ?)''', (filehash,))

			result = c.fetchone()

		if result:
			filehash, path, rank = result
			return rank
		else:
			return None



class ELOSort:
	def __init__(self, db):
		self.db = db

	def index(self, winner=None, loser=None):
		if winner and loser:


			

			if sort_by != '':
				results.sort(key=attrgetter(sort_by), reverse=sort_reverse)

		return """<html><b>%s</b> beat <b>%s</b></html>""" % (winner, loser)

	index.exposed = True




if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option("--emgfile", dest="emgfile",
					help="EMG trace file name", metavar="FILE")

	(opts, args) = parser.parse_args()

	print opts, args

	if args:
		basedir = args[0]
	else:
		basedir = "."


	filename = os.path.join(basedir, ".elosortdb.sql3")


	cherrypy.quickstart(ELOSort())