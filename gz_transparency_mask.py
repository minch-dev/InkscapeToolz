#!/usr/bin/env python 
'''
transform transparency into masks
'''
import inkex,simplestyle,colorsys,copy
import random,math,re,bezmisc,cubicsuperpath
from simpletransform import *

def alpha_to_grey(alpha):
	r,g,b = colorsys.hls_to_rgb(0,alpha,0)
	return 'rgb(%d,%d,%d)'%( round(r*255),round(g*255),round(b*255) )

def opaqify(self,node):
	style = simplestyle.parseStyle(node.get('style'))
	style['opacity'] = 1.0
	style['fill-opacity'] = 1.0
	style['stroke-opacity'] = 1.0
	for attrib in ['fill','stroke']:
		if style.has_key(attrib):
			fill = style[attrib]
			if(fill != 'none' and fill.startswith('url(#')):
				gradient_wrapper = self.xpathSingle( "//*[@id='%s']" % (fill[len('url(#'):fill.find(')')]) )
				if gradient_wrapper.tag != inkex.addNS('pattern','svg'):
					gradient = self.xpathSingle( "//*[@id='%s']" %(gradient_wrapper.get(inkex.addNS("href", "xlink"))[1:]) ) 
					for stop in gradient:
						stop_style = simplestyle.parseStyle(stop.get('style'))
						stop_style['stop-opacity'] = 1.0
						stop.set('style', simplestyle.formatStyle(stop_style))

	node.set('style', simplestyle.formatStyle(style))

def check_transparency(self,style):
	transparent = False
	if style.has_key('opacity'):
		if float(style['opacity']) < 1.0:
			transparent = True
		
	if style.has_key('fill-opacity'):
		if float(style['fill-opacity']) < 1.0:
			transparent = True
		
	if style.has_key('stroke-opacity'):
		if float(style['stroke-opacity']) < 1.0:
			transparent = True
		
	if style.has_key('fill'):
		fill = style['fill']
		if(fill != 'none'):
			if fill.startswith('url(#'):
				gradient_id = fill[len('url(#'):fill.find(')')]
				gradient = self.xpathSingle("//*[@id='%s']" % gradient_id)
				if gradient.tag != inkex.addNS('pattern','svg'):
					url_stops = gradient.get(inkex.addNS("href", "xlink"))
					gradient_stops = self.xpathSingle("//svg:linearGradient[@id='%s']" % url_stops[1:])
					for stop in gradient_stops:
						stop_style = simplestyle.parseStyle(stop.get('style'))
						if stop_style.has_key('stop-opacity'):
							if float(stop_style['stop-opacity']) < 1.0:
								transparent = True
		
	if style.has_key('stroke'):
		stroke = style['stroke']
		if(stroke != 'none'):
			if stroke.startswith('url(#'):
				gradient_id = stroke[len('url(#'):stroke.find(')')]
				gradient = self.xpathSingle("//*[@id='%s']" % gradient_id)
				if gradient.tag != inkex.addNS('pattern','svg'):
					url_stops = gradient.get(inkex.addNS("href", "xlink"))
					gradient_stops = self.xpathSingle("//svg:linearGradient[@id='%s']" % url_stops[1:])
					for stop in gradient_stops:
						stop_style = simplestyle.parseStyle(stop.get('style'))
						if stop_style.has_key('stop-opacity'):
							if float(stop_style['stop-opacity']) < 1.0:
								transparent = True
		
	return transparent


def mask(self,node):
	defs = self.xpathSingle("//svg:defs")
	base_alpha = 1.0
	style = simplestyle.parseStyle(node.get('style'))
	transparent = check_transparency(self,style)
	
	grey_mask = copy.deepcopy(node)
	grey_mask_id = node.get('id')+'Grey'
	grey_mask.set('id', grey_mask_id)
	grey_mask_style = simplestyle.parseStyle(grey_mask.get('style'))
	
	if style.has_key('opacity'):
		opacity = float(style['opacity'])
		base_alpha *= opacity;

	for attrib in ['fill','stroke']:
		if style.has_key(attrib):
			fill_alpha = 1.0
			fill = style[attrib]
			if(fill != 'none'):
				if style.has_key(attrib+'-opacity'):
					opacity = float(style[attrib+'-opacity'])
					fill_alpha *= opacity;
			
				if fill.startswith('url(#'):
					custom_gradient_id = fill[len('url(#'):fill.find(')')]
					custom_gradient = self.xpathSingle("//*[@id='%s']" % custom_gradient_id)
					
					gradient_id = custom_gradient.get(inkex.addNS("href", "xlink"))[1:]
					gradient = self.xpathSingle("//*[@id='%s']" % gradient_id)
					
					#opacify gradient
					gradient_opaque_id = gradient_id+'Opaque'
					try:
						gradient_opaque = self.xpathSingle("//*[@id='%s']" % gradient_opaque_id)
					except:
						gradient_opaque = copy.deepcopy(gradient)
						gradient_opaque.set('id', gradient_opaque_id)
						defs.append(gradient_opaque)
					custom_gradient.set(inkex.addNS("href", "xlink"), '#'+gradient_opaque_id)
					
					
					grey_gradient_id = custom_gradient_id+'Mask'
					try:
						grey_gradient = self.xpathSingle("//*[@id='%s']" % grey_gradient_id)
						grey_gradient.getParentNode().removeChild(grey_gradient);
					except:
						pass
					grey_gradient = copy.deepcopy(gradient)
					grey_gradient.set('id', grey_gradient_id)
					defs.append(grey_gradient)
					
					
					grey_custom_gradient_id = custom_gradient_id+'Local'
					try:
						grey_custom_gradient = self.xpathSingle("//*[@id='%s']" % grey_custom_gradient_id)
						grey_custom_gradient.getParentNode().removeChild(grey_custom_gradient);
					except:
						pass
					grey_custom_gradient = copy.deepcopy(custom_gradient)
					grey_custom_gradient.set('id', grey_custom_gradient_id)
					defs.append(grey_custom_gradient)
					grey_custom_gradient.set(inkex.addNS("href", "xlink"), '#'+grey_gradient_id)
					
					
					for stop in grey_gradient:
						stop_style = simplestyle.parseStyle(stop.get('style'))
						stop_style['stop-color'] = alpha_to_grey(base_alpha*fill_alpha)
						#white or base grey
						if stop_style.has_key('stop-opacity'):
							if float(stop_style['stop-opacity']) < 1.0:
								stop_style['stop-color'] = alpha_to_grey(base_alpha*fill_alpha*float(stop_style['stop-opacity']))
								stop_style['stop-opacity'] = 1.0
								#grey
						stop.set('style', simplestyle.formatStyle(stop_style))
						#colors.append(stop.get("style"))
					grey_mask_style[attrib] = 'url(#'+grey_custom_gradient_id+')'
				else:
					grey_mask_style[attrib] = alpha_to_grey(base_alpha*fill_alpha)

	
	grey_mask.set('style', simplestyle.formatStyle(grey_mask_style))
	mask_wrapper = inkex.etree.Element(inkex.addNS('mask','svg'))
	mask_wrapper.set('id',grey_mask_id+'Mask')
	mask_wrapper.set('maskUnits','userSpaceOnUse')
	mask_wrapper.append(grey_mask)
	defs.append(mask_wrapper)
	
	style['mask'] = 'url(#'+grey_mask_id+'Mask'+')'
	node.set('style', simplestyle.formatStyle(style))
	opaqify(self,node)
	opaqify(self,grey_mask)



	
class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		svg = self.document.getroot()
		for id,node in self.selected.iteritems():
			style = simplestyle.parseStyle(node.get('style'))
			if check_transparency(self,style):
				if node.tag == inkex.addNS('rect','svg'):
					node = self.rectToPath(node,True)
				else:
					if node.get('sodipodi:cx')!='None' or node.get('cx')!='None':
						node = self.objectToPath(node,True)

				mask(self,node)


	

	

#Creator: Inkscape 0.91 rev.13725
################################
#-- Object utils ----------
################################
	def uniqueId(self, prefix):
		id="%s%04i"%(prefix,random.randint(0,9999))
		while len(self.document.getroot().xpath('//*[@id="%s"]' % id,namespaces=inkex.NSS)):
			id="%s%04i"%(prefix,random.randint(0,9999))
		return(id)

	def recursNewIds(self,node):
		if node.get('id'):
			node.set('id',self.uniqueId(node.tag))
		for child in node:
			self.recursNewIds(child)
			
	def refNode(self,node):
		if node.get(inkex.addNS('href','xlink')):
			refid=node.get(inkex.addNS('href','xlink'))
			path = '//*[@id="%s"]' % refid[1:]
			newNode = self.document.getroot().xpath(path, namespaces=inkex.NSS)[0]
			return newNode
		else:
			raise AssertionError, "Trying to follow empty xlink.href attribute."

	def unlinkClone(self,node,doReplace):
		if node.tag == inkex.addNS('use','svg') or node.tag=='use':
			newNode = copy.deepcopy(self.refNode(node))
			self.recursNewIds(newNode)
			applyTransformToNode(parseTransform(node.get('transform')),newNode)

			if doReplace:
				parent=node.getparent()
				parent.insert(parent.index(node),newNode)
				parent.remove(node)

			return newNode
		else:
			raise AssertionError, "Only clones can be unlinked..."

	def unlinkClone(self,node,doReplace):
		if node.tag == inkex.addNS('use','svg') or node.tag=='use':
			newNode = copy.deepcopy(self.refNode(node))
			self.recursNewIds(newNode)
			applyTransformToNode(parseTransform(node.get('transform')),newNode)

			if doReplace:
				parent=node.getparent()
				parent.insert(parent.index(node),newNode)
				parent.remove(node)

			return newNode
		else:
			raise AssertionError, "Only clones can be unlinked..."
			
################################
#-- Object conversion ----------
################################
	def rectToPath(self,node,doReplace=True):
		if node.tag == inkex.addNS('rect','svg'):
			x =float(node.get('x'))
			y =float(node.get('y'))
			#FIXME: no exception anymore and sometimes just one
			try:
				rx=float(node.get('rx'))
				ry=float(node.get('ry'))
			except:
				rx=0
				ry=0
			w =float(node.get('width' ))
			h =float(node.get('height'))
			d ='M %f,%f '%(x+rx,y)
			d+='L %f,%f '%(x+w-rx,y)
			d+='A %f,%f,%i,%i,%i,%f,%f '%(rx,ry,0,0,1,x+w,y+ry)
			d+='L %f,%f '%(x+w,y+h-ry)
			d+='A %f,%f,%i,%i,%i,%f,%f '%(rx,ry,0,0,1,x+w-rx,y+h)
			d+='L %f,%f '%(x+rx,y+h)
			d+='A %f,%f,%i,%i,%i,%f,%f '%(rx,ry,0,0,1,x,y+h-ry)
			d+='L %f,%f '%(x,y+ry)
			d+='A %f,%f,%i,%i,%i,%f,%f '%(rx,ry,0,0,1,x+rx,y)

			newnode=inkex.etree.Element('path')
			newnode.set('d',d)
			newnode.set('id', self.uniqueId('path'))
			newnode.set('style',node.get('style'))
			nnt = node.get('transform')
			if nnt:
				newnode.set('transform',nnt)
				fuseTransform(newnode)
			if doReplace:
				parent=node.getparent()
				parent.insert(parent.index(node),newnode)
				parent.remove(node)
			return newnode

	def groupToPath(self,node,doReplace=True):
		if node.tag == inkex.addNS('g','svg'):
			newNode = inkex.etree.SubElement(self.current_layer,inkex.addNS('path','svg'))    

			newstyle = simplestyle.parseStyle(node.get('style') or "")
			newp = []
			for child in node:
				childstyle = simplestyle.parseStyle(child.get('style') or "")
				childstyle.update(newstyle)
				newstyle.update(childstyle)
				childAsPath = self.objectToPath(child,False)
				newp += cubicsuperpath.parsePath(childAsPath.get('d'))
			newNode.set('d',cubicsuperpath.formatPath(newp))
			newNode.set('style',simplestyle.formatStyle(newstyle))

			self.current_layer.remove(newNode)
			if doReplace:
				parent=node.getparent()
				parent.insert(parent.index(node),newNode)
				parent.remove(node)

			return newNode
		else:
			raise AssertionError
		
	def objectToPath(self,node,doReplace=True):
		#--TODO: support other object types!!!!
		#--TODO: make sure cubicsuperpath supports A and Q commands... 
		if node.tag == inkex.addNS('rect','svg'):
			return(self.rectToPath(node,doReplace))
		if node.tag == inkex.addNS('g','svg'):
			return(self.groupToPath(node,doReplace))
		elif node.tag == inkex.addNS('path','svg') or node.tag == 'path':
			#remove inkscape attributes, otherwise any modif of 'd' will be discarded!
			for attName in node.attrib.keys():
				if ("sodipodi" in attName) or ("inkscape" in attName):
					del node.attrib[attName]
			fuseTransform(node)
			return node
		elif node.tag == inkex.addNS('use','svg') or node.tag == 'use':
			newNode = self.unlinkClone(node,doReplace)
			return self.objectToPath(newNode,doReplace)
		else:
			inkex.errormsg("Please first convert objects to paths!  (Got [%s].)"% node.tag)
			return None

	def objectsToPaths(self,aList,doReplace=True):
		newSelection={}
		for id,node in aList.items():
			newnode=self.objectToPath(node,doReplace)
			del aList[id]
			aList[newnode.get('id')]=newnode


if __name__ == '__main__':
	e = Lust()
	e.affect()


