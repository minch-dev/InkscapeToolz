import inkex,simplestyle,colorsys,copy
import random,math,re,bezmisc,cubicsuperpath
from simpletransform import *

class Grabz(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def computeBBox(aList,mat=[[1,0,0],[0,1,0]]):
		bbox=None
		for node in aList:
			m = parseTransform(node.get('transform'))
			m = composeTransform(mat,m)
			#TODO: text not supported!
			d = None
			if node.get("d"):
				d = node.get('d')
			elif node.get('points'):
				d = 'M' + node.get('points')
			elif node.tag in [ inkex.addNS('rect','svg'), 'rect', inkex.addNS('image','svg'), 'image' ]:
				d = 'M' + node.get('x', '0') + ',' + node.get('y', '0') + \
					'h' + node.get('width') + 'v' + node.get('height') + \
					'h-' + node.get('width')
			elif node.tag in [ inkex.addNS('text','svg'), 'text', inkex.addNS('tspan','svg'), 'tspan' ]:
				d = 'M' + node.get('x', '0') + ',' + node.get('y', '0') + \
					'h' + '0.0' + 'v' + '0.0' + \
					'h-' + '0.0'
			elif node.tag in [ inkex.addNS('line','svg'), 'line' ]:
				d = 'M' + node.get('x1') + ',' + node.get('y1') + \
					' ' + node.get('x2') + ',' + node.get('y2')
			elif node.tag in [ inkex.addNS('circle','svg'), 'circle', \
								inkex.addNS('ellipse','svg'), 'ellipse' ]:
				rx = node.get('r')
				if rx is not None:
					ry = rx
				else:
					rx = node.get('rx')
					ry = node.get('ry')
				cx = float(node.get('cx', '0'))
				cy = float(node.get('cy', '0'))
				x1 = cx - float(rx)
				x2 = cx + float(rx)
				d = 'M %f %f ' % (x1, cy) + \
					'A' + rx + ',' + ry + ' 0 1 0 %f,%f' % (x2, cy) + \
					'A' + rx + ',' + ry + ' 0 1 0 %f,%f' % (x1, cy)
	 
			if d is not None:
				p = cubicsuperpath.parsePath(d)
				applyTransformToPath(m,p)
				bbox=boxunion(refinedBBox(p),bbox)

			elif node.tag == inkex.addNS('use','svg') or node.tag=='use':
				refid=node.get(inkex.addNS('href','xlink'))
				path = '//*[@id="%s"]' % refid[1:]
				refnode = node.xpath(path)
				bbox=boxunion(computeBBox(refnode,m),bbox)
				
			bbox=boxunion(computeBBox(node,m),bbox)
		return bbox

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
