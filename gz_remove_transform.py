#!/usr/bin/env python 
'''
select open paths
'''
import inkex

class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		svg = self.document.getroot()
		if len(self.selected)>0 :
			for i,p in self.selected.iteritems():
				transform = p.get('transform')
				if transform != None:
					del p.attrib["transform"]

if __name__ == '__main__':
	e = Lust()
	e.affect()


