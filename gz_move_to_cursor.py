#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re
from grabz import *

class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		root = self.document.getroot()
		doc_width = float(self.unittouu(root.get('width')))
		doc_height = float(self.unittouu(root.get('height')))
		namedview = root.find(inkex.addNS('namedview', 'sodipodi'))
		cx = float( namedview.get(inkex.addNS('cx', 'inkscape')) )
		cy = doc_height - float( namedview.get(inkex.addNS('cy', 'inkscape')) )
		#works for any element except for those that have scale applied to original group
		if len(self.selected)>0 :
			xxyy = computeBBox(self.selected.values())
			translate_x = xxyy[0]-cx
			translate_y = xxyy[3]-cy
			#inkex.debug( 'cx:%f cy:%f x:%f y:%f' % (cx,cy,xxyy[0],xxyy[3]) )
			tranform_before = ''


			for id, node in self.selected.iteritems():
				
				#if node.tag == inkex.addNS('g','svg'):
				for clone in root.xpath('//svg:use[@xlink:href="#%s"]' % id, namespaces=inkex.NSS):
					clone_transform = clone.get('transform')
					if clone_transform == None:
						clone_transform = ''
					clone.set( 'transform', '%s translate(%f,%f)' % (clone_transform,translate_x,translate_y) )
				tranform_before = node.get('transform')
				if tranform_before == None:
					tranform_before = ''
				node.set( 'transform', '%s translate(%f,%f)' % (tranform_before,-translate_x,-translate_y) )

if __name__ == '__main__':
	e = Lust()
	e.affect()