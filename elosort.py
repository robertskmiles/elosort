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
		self.dbfile = dbfile
		try:
			open(self.dbfile)
			con = sqlite3.connect(self.dbfile)
			print "\""+self.dbfile+"\" found :)"
		except IOError:
			print "\""+self.dbfile+"\" not found, making a new one"
			con = sqlite3.connect(self.dbfile)
			c = con.cursor()
			c.execute('''create table Item
						(hash text PRIMARY_KEY, path text, rank integer)''')
			con.commit()
			c.close()
			con.close()

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

		con = sqlite3.connect(self.dbfile)
		c = con.cursor()
		c.execute('''SELECT rank from Item
						where hash = ?''', (filehash,))

		result = c.fetchone()
		c.close()
		con.close()

		if result:
			rank = result[0]
			return rank
		else:
			self.initrank(filepath)
			return STARTRANK

	def setrank(self, filepath, newrank):
		filehash = self.filehash(filepath)

		con = sqlite3.connect(self.dbfile)
		c = con.cursor()
		c.execute("""UPDATE Item
					SET path = ?, rank = ? WHERE hash = ?""",
					(filepath, newrank, filehash))

		con.commit()
		c.close()
		con.close()

	def initrank(self, filepath):
		"""Add a new file to the db, with the starting rank"""
		filehash = self.filehash(filepath)
		abspath = os.path.abspath(filepath)

		con = sqlite3.connect(self.dbfile)
		c = con.cursor()
		c.execute('''INSERT into Item values (?, ?, ?)''',
					(filehash, abspath, STARTRANK))

		con.commit()
		c.close()
		con.close()


class Itemcollection:
	def __init__(self, items):
		self.items = items
		self.shuffle()

	def shuffle(self):
		self.itemstack = self.items[:]
		random.shuffle(self.itemstack)

	def next(self):
		if not self.itemstack:
			self.shuffle()

		return self.itemstack.pop()


template = '''
<html>
<head>
	<script language="javascript" type="text/javascript">
		document.onkeyup = KeyPressed;

		function KeyPressed( e ) {
			var key = ( window.event ) ? event.keyCode : e.keyCode;

			switch( key ) {
				case 37: //left
					window.location.href="/?a=%(im1)s&b=%(im2)s&result=1"
					break;
				case 39: //right
					window.location.href="/?a=%(im2)s&b=%(im1)s&result=1"
					break;
			}
		}
	</script>
</head>
<body>
	<a href="/?a=%(im1)s&b=%(im2)s&result=1"><img src="static/%(im1)s" width="49%%"></a>
	<a href="/?a=%(im2)s&b=%(im1)s&result=1"><img src="static/%(im2)s" width="49%%"></a>
</body>
</html>
'''


class ELOSort:
	def __init__(self, db, items):
		self.db = db
		self.items = items

	def index(self, a=None, b=None, result=None):
		if a and b and result:
			if result in ("0", "1", "0.5"):
				self.match(a, b, float(result))
			else:
				return "Invalid value for result"

		vars = {
			"im1" : self.items.next(),
			"im2" : self.items.next()
		}

		return template % vars

	index.exposed = True

	def match(self, a, b, result):
		k = 16
		arank = self.db.getrank(a)
		brank = self.db.getrank(b)
		expected = 1 / (1 + (10 ** ((brank - arank) / 400.)))

		newarank = arank + (k * (result - expected))
		newbrank = brank - (k * (result - expected))

		self.db.setrank(a, newarank)
		self.db.setrank(b, newbrank)


if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option("--dbname", dest="dbname", default=".elosortdb.sql3",
					help="Name of ranking database file", metavar="NAME")
	parser.add_option("--filetypes", dest="filetypes", default="jpg,png,gif",
					help="comma separated list of file extensions", metavar="LIST")


	(opts, args) = parser.parse_args()

	if args:
		basedir = args[0]
	else:
		basedir = "."

	basedir = os.path.abspath(basedir)

	dbfilename = os.path.join(basedir, opts.dbname)
	db = ELODB(dbfilename)


	filetypes = opts.filetypes.split(",")
	items = []
	for filetype in filetypes:
		items += glob.glob(os.path.join(basedir, "*."+filetype))
	itemcollection = Itemcollection(items)

	conf = {'/static': {'tools.staticdir.on': True,
						'tools.staticdir.dir': "/"
						}
			}

	cherrypy.quickstart(ELOSort(db, itemcollection), "/", config=conf)
