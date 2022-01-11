#!/usr/bin/env python
import inkex
import re,string,simpletransform
from grabz import *
from grabz_affine import *
trans_pattern = re.compile('translate\(([-0-9\.]+),([-0-9\.]+)\)')
matrix_pattern = re.compile('matrix\(([-0-9\.\,]+)\)')
# affine
# a, b, c, d, e, f,
# Affine.column_vectors
# ((a, d), (b, e), (c, f))
 
# svg matrix
# (a,d,b,e,c,f)
# a[0],a[3],a[1],a[4],a[2],a[4]

# simpletransform
# [[a, b, c], [d, e, f]]
		#inkex.debug( swapem.svg_matrix_to_affine(self,'translate(-5,9)'))
		#inkex.debug( swapem.affine_to_svg_matrix(self, Affine(0.1,0.2,0.3,0.4,0.5,0.6) ) )
		#inkex.debug( simpletransform.parseTransform('translate(-5,9)') )
		#inkex.debug( simpletransform.parseTransform('translate(-5,9) matrix(0.80466295,0.59373187,-0.59373187,0.80466295,720.73149,1118.4722)') )
		#inkex.debug( Affine.__invert__(Affine.translation(-5,9)) )
		#inkex.debug( Affine.translation(-5,9).__mul__(Affine.translation(5,-9)) )


class swapem(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--symbol_id_old", action="store", type="string", dest="symbol_id_old", help="")
		self.OptionParser.add_option("--symbol_id_new", action="store", type="string", dest="symbol_id_new", help="")
		self.OptionParser.add_option("--apply_to_selected", action="store", type="inkbool", dest="apply_to_selected", help="")
		self.OptionParser.add_option("--return_text_only", action="store", type="inkbool", dest="return_text_only", help="")
	def affine_to_svg_matrix(self,a):
		return 'matrix(%f,%f,%f,%f,%f,%f)' % (a[0],a[3],a[1],a[4],a[2],a[5])

	def svg_matrix_to_affine(self,matrix_string):
		s = simpletransform.parseTransform(matrix_string)
		return Affine(s[0][0],s[0][1],s[0][2],s[1][0],s[1][1],s[1][2])
	
	def effect(self):
		debug = True

		global trans_pattern
		symbol_id_old = str(self.options.symbol_id_old)
		symbol_id_new = str(self.options.symbol_id_new)
		apply_to_selected = bool(self.options.apply_to_selected)
		return_text_only = bool(self.options.return_text_only)
		root = self.document.getroot()
		new_symbol = root.xpath('//*[@id="%s"]' % symbol_id_new, namespaces=inkex.NSS)
		if(len(new_symbol)==1):
			if(new_symbol[0].tag == inkex.addNS('g','svg')):
				new_symbol_xxyy = computeBBox(new_symbol)
				new_symbol = new_symbol[0]
				new_symbol_pos_x = float(new_symbol_xxyy[0])
				new_symbol_pos_y = float(new_symbol_xxyy[2])
				new_symbol_object_center_x = (float(new_symbol_xxyy[1]) - float(new_symbol_xxyy[0]))/2 + float(new_symbol_xxyy[0])
				new_symbol_object_center_y = (float(new_symbol_xxyy[3]) - float(new_symbol_xxyy[2]))/2 + float(new_symbol_xxyy[2])
				new_symbol_rotation_center_x = new_symbol.get(inkex.addNS('transform-center-x','inkscape'))
				new_symbol_rotation_center_y = new_symbol.get(inkex.addNS('transform-center-y','inkscape'))
				if None == new_symbol_rotation_center_x:
					new_symbol_rotation_center_x = 0.0;
				else:
					new_symbol_rotation_center_x = float(new_symbol_rotation_center_x);
				if None == new_symbol_rotation_center_y:
					new_symbol_rotation_center_y = 0.0;
				else:
					new_symbol_rotation_center_y = float(new_symbol_rotation_center_y);
				new_symbol_absolute_rotation_center_x = new_symbol_object_center_x+new_symbol_rotation_center_x
				new_symbol_absolute_rotation_center_y = new_symbol_object_center_y-new_symbol_rotation_center_y
				new_symbol_absolute_rotation_center_affine = Affine.translation(new_symbol_absolute_rotation_center_x,new_symbol_absolute_rotation_center_y)
			else:
				raise AssertionError, "the symbol is not a group"
				return False
		else:
			raise AssertionError, "there is no symbol with that id"
			return False
		if len(self.selected)>0:
			
			for i,node in self.selected.iteritems():
			
				if node.tag == inkex.addNS('use','svg'):
					if node.get(inkex.addNS('href','xlink')):
						refid=node.get(inkex.addNS('href','xlink'))
						path = '//*[@id="%s"]' % refid[1:]
						src_symbol = root.xpath(path, namespaces=inkex.NSS)
						xxyy = computeBBox(src_symbol)
						src_symbol = src_symbol[0]
						#need a find and replace mode
						src_symbol_pos_x = float(xxyy[0])
						src_symbol_pos_y = float(xxyy[2])
						
						src_symbol_rotation_center_x = src_symbol.get(inkex.addNS('transform-center-x','inkscape'))
						src_symbol_rotation_center_y = src_symbol.get(inkex.addNS('transform-center-x','inkscape'))
						if None == src_symbol_rotation_center_x:
							src_symbol_rotation_center_x = 0.0;
						else:
							src_symbol_rotation_center_x = float(src_symbol_rotation_center_x);
						src_symbol_rotation_center_y = src_symbol.get(inkex.addNS('transform-center-y','inkscape'))
						if None == src_symbol_rotation_center_y:
							src_symbol_rotation_center_y = 0.0;
						else:
							src_symbol_rotation_center_y = float(src_symbol_rotation_center_y);
						
						src_symbol_object_center_x = (float(xxyy[1]) - float(xxyy[0]))/2 + float(xxyy[0])
						src_symbol_object_center_y = (float(xxyy[3]) - float(xxyy[2]))/2 + float(xxyy[2])
						src_symbol_absolute_rotation_center_x = src_symbol_object_center_x+src_symbol_rotation_center_x
						src_symbol_absolute_rotation_center_y = src_symbol_object_center_y-src_symbol_rotation_center_y
						transform = node.get('transform')
						if None == transform:
							transform = ''
						delta_pos_x = src_symbol_absolute_rotation_center_x - new_symbol_absolute_rotation_center_x
						delta_pos_y = src_symbol_absolute_rotation_center_y - new_symbol_absolute_rotation_center_y
						transform_affine = swapem.svg_matrix_to_affine(self,transform) * Affine.translation(delta_pos_x,delta_pos_y)
						transform = swapem.affine_to_svg_matrix(self,  transform_affine)

						#inkex.debug(return_text_only)
						
						if(return_text_only <> True):
							
							node.set('transform', transform)
							node.set(inkex.addNS('href','xlink'), '#'+symbol_id_new)
							
							if(new_symbol_rotation_center_x <>0.0 or new_symbol_rotation_center_y <>0.0):
							#compute new bbox, new center, then inkscape-specific coordinates
							#we need to apply all parents' transforms to determine actual rotation position
							# * parents_transforms_affine
							#for some reason it's not even necessary
								# parents_transforms_list = []
								# parent = node.getparent()
								# while parent.get(inkex.addNS('groupmode','inkscape')) <> 'layer':
									# parent_transform = parent.get('transform')
									# if None != parent_transform:
										# parents_transforms_list.append(swapem.svg_matrix_to_affine(self,parent_transform))
									# parent = parent.getparent()
									# if parent == None:
										# break
								# parents_transforms_affine = Affine.identity()
								# parents_transforms_list.reverse()
								# for parent_affine in parents_transforms_list:
									# parents_transforms_affine = parents_transforms_affine * parent_affine
								
								node_center_affine = transform_affine * new_symbol_absolute_rotation_center_affine
								xxyy = computeBBox([node])
								node_center_x = (float(xxyy[1]) - float(xxyy[0]))/2 + float(xxyy[0])
								node_center_y = (float(xxyy[3]) - float(xxyy[2]))/2 + float(xxyy[2])
								
								node_rotation_x = node_center_affine[2] - node_center_x
								node_rotation_y = -(node_center_affine[5] - node_center_y)
								node.set(inkex.addNS('transform-center-x','inkscape'), str(node_rotation_x))
								node.set(inkex.addNS('transform-center-y','inkscape'), str(node_rotation_y))


							# inkex.debug((real_pos_x,real_pos_y))
							# inkex.debug((tran_pos_x,tran_pos_y))
							#inkex.debug((delta_pos_x,delta_pos_y))
							# if not(delta_pos_x==0 and delta_pos_y==0):
								# for node in cln.xpath('./*', namespaces=inkex.NSS):
									# node_transform = node.get('transform')
									# if node_transform == None:
										# node_transform = ''
									
								# cln.set('transform','translate(%f,%f)' % (real_pos_x,real_pos_y) )
						
						else:
							inkex.debug('#'+symbol_id_new)
							inkex.debug(transform)
							
						

					else:
						raise AssertionError, "Trying to follow empty xlink.href attribute."
if __name__ == '__main__':
	e = swapem()
	e.affect()

