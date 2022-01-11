#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,simplestyle



def deleteAllGuides(document):
	nv = document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]
	children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',namespaces=inkex.NSS)
	for element in children:
			nv.remove(element)

def delete_refs(self,id):
	svg = self.document.getroot()
	for pp in svg.xpath('//*[@style]', namespaces=inkex.NSS):
		style = simplestyle.parseStyle(pp.get('style'))
		if 'fill' in style:
			if style['fill'] == 'url(#%s)'%id :
				style['fill'] = '#000000'
		if 'stroke' in style:
			if style['stroke'] == 'url(#%s)'%id :
				style['stroke'] = '#000000'
		pp.set('style', simplestyle.formatStyle(style))

def delete_xlink_refs(self,id):
	svg = self.document.getroot()
	for pp in svg.xpath('//*[@xlink:href]', namespaces=inkex.NSS):
		link = pp.get(inkex.addNS('href','xlink'))
		if link == '#%s'%id :
			if pp.tag == inkex.addNS('use','svg'):
				pp.getparent().remove( pp )
			else:
				pp.set(inkex.addNS('href','xlink'),'')
		

			
class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		svg = self.document.getroot()
		deleteAllGuides(self.document)
		if len(self.selected)<=0 :
			for p in svg.xpath('//svg:image', namespaces=inkex.NSS):
				id = p.get('id')
				# <use>
				for pp in svg.xpath("//*[@xlink:href='#%s']"%id, namespaces=inkex.NSS):
					pp.getparent().remove( pp )
				p.getparent().remove( p )
			for p in svg.xpath('//svg:pattern', namespaces=inkex.NSS):
				id = p.get('id')
				delete_refs(self,id)
				p.getparent().remove( p )
			
		else :
			for i,p in self.selected.iteritems():
				if p.tag == inkex.addNS('image','svg'):
				#todo: children of g
					p.getparent().remove( p )


if __name__ == '__main__':
	e = Lust()
	e.affect()


