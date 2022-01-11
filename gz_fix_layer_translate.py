#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import re,string,simplepath,simplestyle
trans_pattern = re.compile('translate\(([-0-9\.]+),([-0-9\.]+)\)')
matrix_pattern = re.compile('matrix\(([-0-9\.\,]+)\)')

class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		svg = self.document.getroot()
		global trans_pattern
		#[contains(@transform, "translate")]		svg:svg/
		for layer in svg.xpath('//svg:g[@inkscape:groupmode="layer"][contains(@transform, "translate")]', namespaces=inkex.NSS): 
			transform = layer.get('transform')
			if transform == None:
				continue
			translate = trans_pattern.match(transform)
			if translate == None:
				continue
			#translate mojet byti neskoliko, a essho esti matrix
			tx = translate.group(1)
			ty = translate.group(2)
			tx = float(tx)
			ty = float(ty)
			#'/*[@x] | /*[@y]'		node.get()
			#*[not(self::svg:g)][not(self::svg:path)][not(self::svg:ellipse)][not(self::svg:svg)]
			#inkex.debug(layer.tag+' '+str(tx)+' '+str(ty) )
			# for object in layer.xpath( '*[not(self::svg:g)][not(self::svg:use)][not(self::svg:path)][not(self::svg:ellipse)][not(self::svg:svg)]', namespaces=inkex.NSS):
				# ox = object.get('x')
				# if ox==None:
					# ox = 0.0
				# oy = object.get('y')
				# if oy==None:
					# oy = 0.0					
				# ox = float( ox )
				# oy = float( oy )
				# object.set('x', str(ox+tx))
				# object.set('y', str(oy+ty))
			#for object in layer.xpath('svg:path | svg:g', namespaces=inkex.NSS):
			for object in layer.xpath( '*[not(self::svg:use)][not(self::svg:svg)]', namespaces=inkex.NSS):
				object_transform = object.get('transform')
				replace = False
				ox = 0.0
				oy = 0.0
				if object_transform == None:
					object_transform = ''
				else:
					object_transform = object_transform.strip()
					object_translate = trans_pattern.match(object_transform)
					if (object_translate != None) and (object_transform.find('translate') == 0): #and translate is first
						ox = float( object_translate.group(1) )
						oy = float( object_translate.group(2) )
						replace = True
				
				translate_string = 'translate('+str(ox+tx)+','+str(oy+ty)+')'
				if replace == True:
					object_transform = re.sub(trans_pattern,translate_string,object_transform)
				else:
					object_transform = translate_string+' '+object_transform
				object.set('transform',object_transform)
			# for ellipse in layer.xpath('svg:ellipse', namespaces=inkex.NSS):
				# cx = float( ellipse.get('cx') )
				# cy = float( ellipse.get('cy') )
				# ellipse.set('cx', str(cx+tx))
				# ellipse.set('cy', str(cy+ty))
			transform = re.sub(trans_pattern,'',transform)
			if transform == '' or transform == ' ':
				del layer.attrib["transform"]
			else:
				layer.set('transform',transform)
				

if __name__ == '__main__':
	e = Lust()
	e.affect()


