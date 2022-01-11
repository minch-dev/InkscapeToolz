#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,simplestyle,gz_transparency_mask


def deleteAllGuides(document):
	nv = document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]
	children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',namespaces=inkex.NSS)
	for element in children:
			nv.remove(element)

class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		svg = self.document.getroot()
		deleteAllGuides(self.document)
		if len(self.selected)<=0 :
			for p in svg.xpath('//svg:path | //svg:rect | //svg:ellipse | //svg:g', namespaces=inkex.NSS):
				gz_transparency_mask.opaqify(self,p)
		else :
			for i,p in self.selected.iteritems():
				#todo: children of g
				gz_transparency_mask.opaqify(self,p)

if __name__ == '__main__':
	e = Lust()
	e.affect()


