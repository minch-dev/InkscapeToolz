#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,cubicsuperpath


class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		svg = self.document.getroot()
		if len(self.selected)<=0 :
			for p in svg.xpath('//svg:use', namespaces=inkex.NSS):
				self.remove_use_style(p)
		else :
			for i,p in self.selected.iteritems():
				self.remove_use_style(p)


	def remove_use_style(self,p):
		if(p.get('style')!= None):
			del p.attrib['style']
if __name__ == '__main__':
	e = Lust()
	e.affect()


