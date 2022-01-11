#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,cubicsuperpath


class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--newclass",
			action="store", type="string",
			dest="newclass", 
			help="Enter a new id")

	def effect(self):
		newclass = str(self.options.newclass)
		debug = True
		if len(self.selected)>0 :
			for i,elem in self.selected.iteritems():
				elem.set('class',newclass)

if __name__ == '__main__':
	e = Lust()
	e.affect()


