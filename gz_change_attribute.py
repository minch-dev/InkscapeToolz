#!/usr/bin/env python 
'''
change attribute
'''
import inkex

class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--changeattributename",
			action="store", type="string",
			dest="changeattributename", 
			help="Enter attribute name")
		self.OptionParser.add_option("--changeattributevalue",
			action="store", type="string",
			dest="changeattributevalue", 
			help="Enter attribute value")

	def effect(self):
		changeattributename = str(self.options.changeattributename)
		changeattributevalue = str(self.options.changeattributevalue)
		debug = True
		if len(self.selected)>0 :
			for i,elem in self.selected.iteritems():
				elem.set(changeattributename,changeattributevalue)
				#inkex.debug(elem.get(changeattributename))

if __name__ == '__main__':
	e = Lust()
	e.affect()