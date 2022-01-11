#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,cubicsuperpath


class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option(
			"-n", "--newid",
			action="store", type="string",
			dest="newid", 
			help="Enter a new id")

	def effect(self):
		newid = str(self.options.newid)
		if self.getElementById(newid) != None :
			inkex.errormsg("Id already exists!")
			sys.exit(0)
		#delete whitespaces
		debug = True
		svg = self.document.getroot()
		if len(self.selected)==1 :
			for i,original in self.selected.iteritems():
				oldid = original.get('id')
				for clone in svg.xpath('//svg:use[@xlink:href="#%s"]' % oldid, namespaces=inkex.NSS):
					clone.set(inkex.addNS('href','xlink'),'#%s' % newid)
				original.set('id',newid)

if __name__ == '__main__':
	e = Lust()
	e.affect()


