#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,simplestyle
doc_height = 0
sodi = ''
svg = ''
trans_pattern = re.compile('translate\(([-0-9\.]+),([-0-9\.]+)')

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
	
def deleteAllGuides(document):
	nv = document.xpath('/svg:svg/sodipodi:namedview',namespaces=inkex.NSS)[0]
	children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',namespaces=inkex.NSS)
	for element in children:
			nv.remove(element)

def add_guide(self,p,source):
	global doc_height
	global sodi
	global trans_pattern
	layer = get_layer(p)
	id = p.get('id')
	if layer != None:
		sodi.set(inkex.addNS('current-layer','inkscape'),layer.get('id'))
	if p.tag == inkex.addNS('path','svg'):
		p_arr = simplepath.parsePath(p.get('d'))
		x = str(p_arr[0][1][0])
		y = str(doc_height - p_arr[0][1][1])
	elif p.tag == inkex.addNS('rect','svg') or p.tag == inkex.addNS('image','svg'):
		x = p.get('x')
		y = str( doc_height - float(p.get('y')) )
	elif p.tag == inkex.addNS('use','svg'):
		# source = self.xpathSingle( "//*[@id='%s']" % id )
		x = source.get('x')
		y = str( doc_height - float(source.get('y')) )
	elif p.tag == inkex.addNS('ellipse','svg'):
		x = p.get('cx')
		y = str( doc_height - float(p.get('cy')) )
	else:
		return
	tr = p.get('transform')
	if tr != None:
		txty = trans_pattern.match(tr)
		tx = txty.group(1)
		ty = txty.group(2)
		x = str( float(x) + float(tx) )
		y = str( float(y) - float(ty) )
	#add guides to show the problem
	inkex.etree.SubElement(sodi,inkex.addNS('guide','sodipodi'),{ 'position':x+','+y,'orientation':'0,1',inkex.addNS('label','inkscape'):p.get('id') })
	
	

class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		global doc_height
		global sodi
		global svg
		debug = True
		id = None
		svg = self.document.getroot()
		sodi = svg.xpath('//sodipodi:namedview', namespaces=inkex.NSS)[0]
		doc_height = self.unittouu(self.document.getroot().get('height'))
		#clear named target guides
		deleteAllGuides(self.document)
		for p in svg.xpath('//svg:image', namespaces=inkex.NSS):
			if p.getparent().tag == inkex.addNS('pattern','svg'):
				continue
			id = p.get('id')
			add_guide(self,p,p)
			# <use>
			for pp in svg.xpath("//*[@xlink:href='#%s']"%id, namespaces=inkex.NSS):
				add_guide(self,pp,p)
		for p in svg.xpath('//svg:pattern', namespaces=inkex.NSS):
			id = p.get('id')
			for pp in svg.xpath('//*[@style]', namespaces=inkex.NSS):
				style = simplestyle.parseStyle(pp.get('style'))
				add = False
				if 'fill' in style:
					if style['fill'] == 'url(#%s)'%id :
						add = True
				if 'stroke' in style:
					if style['stroke'] == 'url(#%s)'%id :
						add = True
				if add == True:
					add_guide(self,pp,p)
			for pp in svg.xpath('//*[@xlink:href]', namespaces=inkex.NSS):
				link = pp.get(inkex.addNS('href','xlink'))
				if link == '#%s'%id :
					add_guide(self,pp,p)


if __name__ == '__main__':
	e = Lust()
	e.affect()


