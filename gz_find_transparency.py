#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,simplestyle,gz_transparency_mask



def get_layer(child):
	layer = False
	elem = child
	while True:
		#lastelem = elem
		elem = elem.getparent()
		if elem == None:
			layer = elem
			break
		if elem.get(inkex.addNS('groupmode','inkscape')) == 'layer':
			layer = elem
			break
	return layer
def check_open(p):
	open = True
	str = p.get('d')
	r = re.compile('.+[zZ].*$')
	if(re.search(r, str)) :
		open = False
	return open
	
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
		id = None
		svg = self.document.getroot()
		sodi = svg.xpath('//sodipodi:namedview', namespaces=inkex.NSS)[0]
		doc_height = self.unittouu(self.document.getroot().get('height'))
		#clear named target guides
		deleteAllGuides(self.document)
		for p in svg.xpath('//svg:path | //svg:rect | //svg:ellipse | //svg:g', namespaces=inkex.NSS):
			style = p.get('style')
			if style != None:
				style = simplestyle.parseStyle(style)
			else:
				continue
			if gz_transparency_mask.check_transparency(self,style):
				if p.get(inkex.addNS('groupmode','inkscape')) == 'layer':
					gz_transparency_mask.opaqify(self,p)
					continue
				layer = get_layer(p)
				if layer != None:
					id = layer.get('id')
					if p.tag == inkex.addNS('path','svg'):
						p_arr = simplepath.parsePath(p.get('d'))
						x = str(p_arr[0][1][0])
						y = str(doc_height - p_arr[0][1][1])
					elif p.tag == inkex.addNS('rect','svg'):
						x = p.get('x')
						y = str( doc_height - float(p.get('y')) )
					elif p.tag == inkex.addNS('ellipse','svg'):
						x = p.get('cx')
						y = str( doc_height - float(p.get('cy')) )
					else:
						continue
					sodi.set(inkex.addNS('current-layer','inkscape'),id)
					#add guides to show the problem
					inkex.etree.SubElement(sodi,inkex.addNS('guide','sodipodi'),{'position':x+','+y,'orientation':'0,1',inkex.addNS('label','inkscape'):p.get('id')})



				

if __name__ == '__main__':
	e = Lust()
	e.affect()


