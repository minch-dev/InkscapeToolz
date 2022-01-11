#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,cubicsuperpath

class changestyles(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--newstyle",
			action="store", type="string",
			dest="newstyle", 
			help="Enter a new style")
		self.OptionParser.add_option("--recursive",
			action="store", type="string",
			dest="recursive", 
			help="Recursive")
	def changeit(self,elem,style_string):
		if style_string == '' or style_string == None:
			if elem.get('style') != None:
				del elem.attrib['style']
		else: elem.set('style',style_string)
	def effect(self):
		debug = True
		style_string = str(self.options.newstyle)
		recursive = str(self.options.recursive)
		if recursive in('true','True',1,'1'):
			recursive = True
		else: recursive = False

		if len(self.selected)>0 :
			for i,grp in self.selected.iteritems():
				self.changeit(grp,style_string)
				if recursive == True:
					for node in grp.xpath('.//*', namespaces=inkex.NSS):
						self.changeit(node,style_string)


if __name__ == '__main__':
	e = changestyles()
	e.affect()