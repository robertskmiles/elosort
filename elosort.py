#!/usr/bin/env python

import cherrypy
import sqlite3
from optparse import OptionParser
import os
import hashlib
import glob
import random


STARTRATING = 1000


class Elodb:
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
						(hash text PRIMARY_KEY, path text, rating integer)''')
			con.commit()
			c.close()
			con.close()

	def filehash(self, filepath):
		f = open(filepath)

		m = hashlib.md5()
		m.update(f.read())

		return m.hexdigest()

	def getrating(self, filepath):
		"""
		Get the Elo rating for a given file.

		If the file isn't already in the db, add it with the starting rating
		"""
		filehash = self.filehash(filepath)

		con = sqlite3.connect(self.dbfile)
		c = con.cursor()
		c.execute('''SELECT rating from Item
						where hash = ?''', (filehash,))

		result = c.fetchone()
		c.close()
		con.close()

		if result:
			rating = result[0]
			return rating
		else:
			self.initrating(filepath)
			return STARTRATING

	def setrating(self, filepath, newrating):
		filehash = self.filehash(filepath)

		con = sqlite3.connect(self.dbfile)
		c = con.cursor()
		c.execute("""UPDATE Item
					SET path = ?, rating = ? WHERE hash = ?""",
					(filepath, newrating, filehash))

		con.commit()
		c.close()
		con.close()

	def initrating(self, filepath):
		"""Add a new file to the db, with the starting rating"""
		filehash = self.filehash(filepath)
		abspath = os.path.abspath(filepath)

		con = sqlite3.connect(self.dbfile)
		c = con.cursor()
		c.execute('''INSERT into Item values (?, ?, ?)''',
					(filehash, abspath, STARTRATING))

		con.commit()
		c.close()
		con.close()

	def getresults(self, start=0, count=10):
		con = sqlite3.connect(self.dbfile)
		c = con.cursor()
		c.execute('''SELECT * from Item ORDER BY rating DESC''')

		if start:
			c.fetchmany(start)

		result = c.fetchmany(count)
		c.close()
		con.close()

		fields = ['hash', 'path', 'rating']
		result = [dict(zip(fields, row)) for row in result]
		return result

	def sql(self, query):
		"""
		Run an SQL Query on the database

		Mostly used for testing and provisional features
		"""

		con = sqlite3.connect(self.dbfile)
		c = con.cursor()
		c.execute(query)

		result = c.fetchall()
		c.close()
		con.close()

		return result

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
	<div width="49%%"" style="float:left ;text-align:center;"><a href="static/%(im1)s">View Fullsize</a></div>
	<div width="49%%"" style="float:right;text-align:center;"><a href="static/%(im2)s">View Fullsize</a></div>

	<p align="center"><a href="/results">See Results</a></p>
</body>
</html>
'''


class Elosort:
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
		arating = self.db.getrating(a)
		brating = self.db.getrating(b)
		expected = 1 / (1 + (10 ** ((brating - arating) / 400.)))

		newarating = arating + (k * (result - expected))
		newbrating = brating - (k * (result - expected))

		self.db.setrating(a, newarating)
		self.db.setrating(b, newbrating)

	def results(self, start=0, count=10):
		start = int(start)
		count = int(count)

		litemplate = """<li>
							<a href='static/%(path)s'>
								<img src='static/%(path)s' width='100'></a>
							%(rating)f
						</li>"""

		resultstemplate = "<p><a href='/'>Continue Rating</a></p><ol>%s</ol><a href='?start="+str(start+count)+"'>Next</a>"

		return resultstemplate % "\n".join([litemplate % i for i in self.db.getresults(start, count)])

	results.exposed = True

if __name__ == "__main__":

	parser = OptionParser()
	parser.add_option("--dbname", dest="dbname", default=".elosortdb.sql3",
					help="Name of rating database file", metavar="NAME")
	parser.add_option("--filetypes", dest="filetypes", default="jpg,png,gif",
					help="comma separated list of file extensions", metavar="LIST")
	parser.add_option("--port", dest="port", default=8080, type="int",
					help="Port to run the server on", metavar="PORTNUM")

	(opts, args) = parser.parse_args()

	if args:
		basedir = args[0]
	else:
		basedir = "."

	basedir = os.path.abspath(basedir)

	dbfilename = os.path.join(basedir, opts.dbname)
	db = Elodb(dbfilename)

	filetypes = opts.filetypes.split(",")
	items = []
	for filetype in filetypes:
		items += glob.glob(os.path.join(basedir, "*."+filetype))
	itemcollection = Itemcollection(items)

	conf = {'global': {'server.socket_port': opts.port},
			'/static': {'tools.staticdir.on': True,
						'tools.staticdir.dir': "/"
						}
			}

	cherrypy.quickstart(Elosort(db, itemcollection), "/", config=conf)
