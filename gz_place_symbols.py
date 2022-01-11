#!/usr/bin/env python
import inkex
import re,string,simpletransform
from grabz import *
from grabz_affine import *
trans_pattern = re.compile('translate\(([-0-9\.]+),([-0-9\.]+)\)')
matrix_pattern = re.compile('matrix\(([-0-9\.\,]+)\)')

class placeem(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--symbol_id_to_insert", action="store", type="string", dest="symbol_id_to_insert", help="")
		self.OptionParser.add_option("--copy_object_style", action="store", type="inkbool", dest="copy_object_style", help="")
		self.OptionParser.add_option("--primary_only", action="store", type="inkbool", dest="primary_only", help="")
	def affine_to_svg_matrix(self,a):
		return 'matrix(%f,%f,%f,%f,%f,%f)' % (a[0],a[3],a[1],a[4],a[2],a[5])

	def svg_matrix_to_affine(self,matrix_string):
		s = simpletransform.parseTransform(matrix_string)
		return Affine(s[0][0],s[0][1],s[0][2],s[1][0],s[1][1],s[1][2])
	
	def insert_after(self,element,new_element):
		parent = element.getparent()
		parent.insert(parent.index(element)+1, new_element)
	
	def effect(self):
		debug = True

		global trans_pattern
		symbol_id_to_insert = str(self.options.symbol_id_to_insert)
		copy_object_style = bool(self.options.copy_object_style)
		primary_only = bool(self.options.primary_only)
		
		root = self.document.getroot()
		particle_id = symbol_id_to_insert
		particle = root.xpath('//*[@id="%s"]' % particle_id, namespaces=inkex.NSS)
		if(len(particle)==1):
			particle = particle[0]
			if(particle.tag == inkex.addNS('g','svg')):
				#particle_xxyy = computeBBox([particle])
				
				#if mirrored = h we should add minus to each x coordinate and swap point names accordingly
				#if mirrored = c we should use points from href directly or if it's also mirrored with h or c go there
				
				particle_parent_id = particle.get('primary_parent')
				particle_parent = root.xpath('//*[@id="%s"]' % particle_parent_id, namespaces=inkex.NSS)[0]
				particle_parent_points_container_id = particle_parent.get('points_href')
				particle_parent_points_container = root.xpath('//*[@id="%s"]' % particle_parent_points_container_id, namespaces=inkex.NSS)[0]
				points_mirrored = particle_parent_points_container.get('mirrored')
				particle_point_name = particle.get('primary_point')
				if points_mirrored <> None:
					if points_mirrored == 'c':
						particle_parent_points_container_id = particle_parent_points_container.xpath('./svg:use', namespaces=inkex.NSS)[0].get(inkex.addNS('href','xlink'))[1:]
						particle_parent_points_container = root.xpath('//*[@id="%s"]' % particle_parent_points_container_id, namespaces=inkex.NSS)[0]
						points_mirrored = particle_parent_points_container.get('mirrored')
					if points_mirrored == 'h':
						particle_parent_points_container_id = particle_parent_points_container.xpath('./svg:use', namespaces=inkex.NSS)[0].get(inkex.addNS('href','xlink'))[1:]
						particle_parent_points_container = root.xpath('//*[@id="%s"]' % particle_parent_points_container_id, namespaces=inkex.NSS)[0]
						particle_point_name_reversed = particle_point_name.replace('_left','_[oldleft]').replace('_right','_[oldright]')
						particle_point_name_reversed = particle_point_name_reversed.replace('[oldleft]','right').replace('[oldright]','left')
						particle_point_name = particle_point_name_reversed
				
				particle_point = particle_parent_points_container.xpath('./svg:use[@point_name="%s"]' % particle_point_name, namespaces=inkex.NSS)[0]
				point_names_ordered_list = []
				#!!! now we need an array of point names that are in a queue before our particle
				for point in particle_parent_points_container.xpath('./svg:use[@point_name]', namespaces=inkex.NSS):
					point_name = point.get('point_name')
					if point_name == particle_point_name:
						break
					else:
						point_names_ordered_list.append(point_name)
				point_names_set = set(point_names_ordered_list)
				
				particle_parent_transform = particle_parent.get('transform')
				if particle_parent_transform == None:
					particle_parent_x = 0.0
					particle_parent_y = 0.0
				else:
					particle_parent_txty = trans_pattern.match(particle_parent_transform)
					particle_parent_x = float(particle_parent_txty.group(1))
					particle_parent_y = float(particle_parent_txty.group(2))
				particle_parent_affine = Affine.translation(particle_parent_x,particle_parent_y)
				particle_parent_affine_reversed = Affine.translation(-particle_parent_x,-particle_parent_y)

				particle_point_transform = particle_point.get('transform')
				if particle_point_transform == None:
					particle_point_x = 0.0
					particle_point_y = 0.0
				else:
					particle_point_txty = trans_pattern.match(particle_point_transform)
					particle_point_x = float(particle_point_txty.group(1))
					particle_point_y = float(particle_point_txty.group(2))
					if points_mirrored == 'v':
						particle_point_y = -particle_point_y
					if points_mirrored == 'h':
						particle_point_x = -particle_point_x

				particle_point_affine = Affine.translation(particle_point_x,particle_point_y)
				
				
				particle_transform = particle.get('transform')
				if particle_transform == None:
					particle_x = -0.0
					particle_y = -0.0
				else:
					particle_txty = trans_pattern.match(particle_transform)
					particle_x = float(particle_txty.group(1))
					particle_y = float(particle_txty.group(2))
				particle_affine_reverse = Affine.translation(-particle_x,-particle_y)
				particle_affine = Affine.translation(particle_x,particle_y)
				
			else:
				raise AssertionError, "the symbol is not a group"
				return False
		else:
			raise AssertionError, "there is no symbol with that id"
			return False
		if len(self.selected)>0:
			for i,grp in self.selected.iteritems():
				if grp.tag == inkex.addNS('g','svg'):
					for node in grp.xpath('.//svg:use', namespaces=inkex.NSS):
						clone_source_id=node.get(inkex.addNS('href','xlink'))[1:]
						#if clone_source_id is in a list of possible ids (or just primary id) do the job
						if(clone_source_id == particle_parent_id):
							particle_parent_clone = node
							particle_parent_clone_transform = particle_parent_clone.get('transform')
							if particle_parent_clone_transform == None:
								particle_parent_clone_transform = ''
							particle_parent_clone_affine = self.svg_matrix_to_affine(particle_parent_clone_transform)
							new_particle_affine = particle_affine_reverse * particle_parent_affine * particle_point_affine * particle_parent_clone_affine
							new_particle_transform = self.affine_to_svg_matrix(new_particle_affine)
							new_particle = inkex.etree.Element('use')
							new_particle.set('transform', new_particle_transform)
							if copy_object_style == True:
								new_particle.set('style',particle_parent_clone.get('style'))
							new_particle.set(inkex.addNS('href','xlink'), '#%s' % particle_id)
							new_particle_container = particle_parent_clone.getparent()
							#!!! default insert index is parent's index (particle_parent_clone)
							insert_index = new_particle_container.index(particle_parent_clone)
							for p in new_particle_container.xpath('./svg:use', namespaces=inkex.NSS):
								#get particle point
								point_name = p.get('point_name')
								if point_name == None:
									#if none get src then get primary_point
									particle_src_id = p.get(inkex.addNS('href','xlink'))[1:]
									particle_src = root.xpath('//*[@id="%s"]' % particle_src_id, namespaces=inkex.NSS)[0]
									point_name = particle_src.get('primary_point')
								#if this point is in the array compare its insert index with current insert index
								#!!! now we need to iterate over all items that reside in the same container and if their point name (default or custom) is in our prepared array we check if it's element's insert index is higher than we have, we update this index until we reach the end of container and only then insert our part at that index
								if point_name in point_names_set:
									new_insert_index = new_particle_container.index(p)
									#if it is higher rewrite index
									if insert_index < new_insert_index:
										insert_index = new_insert_index
							#now we have insert index and we can proceed
							new_particle_container.insert(insert_index+1, new_particle)
							#now we need to set the new transform center
							new_rotation_affine =  new_particle_affine * particle_affine
							xxyy = computeBBox([new_particle])
							new_particle_center_x = (float(xxyy[1]) - float(xxyy[0]))/2 + float(xxyy[0])
							new_particle_center_y = (float(xxyy[3]) - float(xxyy[2]))/2 + float(xxyy[2])
							
							new_particle_rotation_x = new_rotation_affine[2] - new_particle_center_x
							new_particle_rotation_y = -(new_rotation_affine[5] - new_particle_center_y)
							new_particle.set(inkex.addNS('transform-center-x','inkscape'), str(new_particle_rotation_x))
							new_particle.set(inkex.addNS('transform-center-y','inkscape'), str(new_particle_rotation_y))
							#to make the script even better we should consider which side the anchor point is in container


if __name__ == '__main__':
	e = placeem()
	e.affect()

