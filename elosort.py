#!/usr/bin/env python

import cherrypy
import sqlite3
from optparse import OptionParser
import sys
import os


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


class ELODB:
	def __init__(self, dbfile):
		try:
			self.conn = sqlite3.connect(dbfile)
			print "\""+dbfile+"\" found :)"
		except IOError:
			print "\""+dbfile+"\" not found, making a new one"
			self.conn = sqlite3.connect(dbfile)
			c = self.conn.cursor()
			c.execute('''create table Item
						(hash text PRIMARY_KEY, path text, rank integer)''')
			self.conn.commit()
			c.close()


class ELOSort:
	def __init__(self):
		pass

	def index(self, winner=None, loser=None):
		if winner and loser:
			c.execute('''select rank from Item
			where hash in (select cheat from taglink
			where tag=?)''', (keyword,) )

			results = [Cheat(cmd,desc,idno=cheatid) for cheatid, cmd, desc in c.fetchall()]

			if sort_by != '':
				results.sort(key=attrgetter(sort_by), reverse=sort_reverse)

		return """<html><b>%s</b> beat <b>%s</b></html>""" % (winner, loser)

	index.exposed = True


cherrypy.quickstart(ELOSort())
