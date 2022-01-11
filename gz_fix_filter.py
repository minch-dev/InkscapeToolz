#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,simplestyle,gz_transparency_mask


def deleteFilters(node):
	style = node.get('style')
	style = simplestyle.parseStyle(style)
	style.pop('filter',None)
	style.pop('display',None)
	style.pop('enable-background',None)
	style.pop('fill-rule',None)
	style.pop('text-rendering',None)
	style.pop('color-rendering',None)
	style.pop('color',None)
	style.pop('shape-rendering',None)
	style.pop('solid-color',None)
	style.pop('color-interpolation-filters',None)
	style.pop('solid-opacity',None)
	style.pop('mix-blend-mode',None)
	style.pop('visibility',None)
	style.pop('clip-rule',None)
	style.pop('image-rendering',None)
	style.pop('overflow',None)
	style.pop('isolation',None)
	style.pop('color-interpolation',None)
	style_string = simplestyle.formatStyle(style)
	node.set('style', style_string)

class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		svg = self.document.getroot()
		if len(self.selected)<=0 :
			for p in svg.xpath('//svg:path | //svg:rect | //svg:ellipse | //svg:g', namespaces=inkex.NSS):
				deleteFilters(p)
		else :
			for i,p in self.selected.iteritems():
				#todo: children of g
				deleteFilters(p)

if __name__ == '__main__':
	e = Lust()
	e.affect()


