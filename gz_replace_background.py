#!/usr/bin/env python
import re,inkex
from grabz import *

def insert_after(element,new_element):
	parent = element.getparent()
	parent.insert(parent.index(element)+1, new_element)
	
class replaceit(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		if len(self.selected)>0 :
			for i,grp in self.selected.iteritems():
				clone = inkex.etree.Element('use')
				clone.set(  inkex.addNS('href','xlink'), '#background')
				grp.insert(0,clone)
		
if __name__ == '__main__':
	e = replaceit()
	e.affect()

