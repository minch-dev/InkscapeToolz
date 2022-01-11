#!/usr/bin/env python 
'''
select open paths
'''
#http://pythex.org/
import inkex
import math,re,simplepath
from simpletransform import *
open_pattern = re.compile('.+[zZ].*$')
single_dot_pattern = re.compile('[Mm] *[-0-9\.]+ *, *[-0-9\.]+ *[Zz]')
single_dot_shape = re.compile('[Mm] *[-0-9\.]+ *, *[-0-9\.]+ *[Cc] *[-0-9\.]+ *, *[-0-9\.]+ *[-0-9\.]+ *, *[-0-9\.]+ * 0,0 *[Zz]')

# M 1351.6598,868.35469 Z
# M 1351.6598,868.35469 Z
# m 1351.6598,868.35469 c -261.4297,29.57565 261.4297,-29.57565 0,0 z
# m 1351.6598,868.35469 c -125.0889,-81.264 115.7558,-94.40426 0,0 z

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
	global open_pattern
	global single_dot_pattern
	open = True
	str = p.get('d')
	if(re.search(open_pattern, str)) :
		open = False
	if(re.search(single_dot_pattern, str)) :
		open = True
	if(re.search(single_dot_shape, str)) :
		open = True
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
		for p in svg.xpath('//svg:path', namespaces=inkex.NSS):
		#for i,p in self.selected.iteritems():
			if check_open(p):
				style = simplestyle.parseStyle(p.get('style'))
				if style.has_key('fill') and style['fill']!='none':
					layer = get_layer(p)
					if layer != None:
						#choose first open path
						id = layer.get('id')
						sodi.set(inkex.addNS('current-layer','inkscape'),id)
					p_arr = simplepath.parsePath(p.get('d'))
					coords = p_arr[0][1]
					#add guides to show the problem
					inkex.etree.SubElement(sodi,inkex.addNS('guide','sodipodi'),{'position':str(coords[0])+','+str(doc_height-coords[1]),'orientation':'0,1',inkex.addNS('label','inkscape'):p.get('id')})
					


				

if __name__ == '__main__':
	e = Lust()
	e.affect()


