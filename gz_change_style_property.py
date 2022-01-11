#!/usr/bin/env python 

import inkex,simplestyle,re
from grabz import *
object_type = 0
open_path_regex = re.compile('.+[zZ].*$')

class deletepropertyfromstyle(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.OptionParser.add_option("--style_prop", action="store", type="string", dest="style_prop", help="")
		self.OptionParser.add_option("--prop_value", action="store", type="string", dest="prop_value", help="")
		self.OptionParser.add_option("--recursive", action="store", type="string", dest="recursive", help="")
		self.OptionParser.add_option("--object_type", action="store", type="string", dest="object_type", help="")
	def change_prop(self,node,prop,value):
		if self.tag_okay(node) == True:
			style = node.get('style')
			if style == None or style == 'None':
				style = ''
			style = simplestyle.parseStyle(style)
			if value == '':
				style.pop(prop,None)
			else:
				style[prop] = value
			node.set('style', simplestyle.formatStyle(style))
	
	def is_open(self,node):
		global open_path_regex
		if(re.search( open_path_regex, node.get('d') )):
			return False
		else: return True
			
	def tag_okay(self,node):
		global object_type
		if object_type == 0:
			return True
		elif object_type ==10:
			if node.tag == inkex.addNS('path','svg'):
				return True
		elif object_type ==11:
			if node.tag == inkex.addNS('path','svg') and self.is_open(node) == True:
				return True
		elif object_type ==12:
			if node.tag == inkex.addNS('path','svg') and self.is_open(node) == False:
				return True
		return False

	def effect(self):
		global object_type
		debug = True
		prop = str(self.options.style_prop)
		value = self.options.prop_value
		if value == None:
			value = ''
		else:
			value = str(value)
		recursive = str(self.options.recursive)
		object_type = int(self.options.object_type)
		if recursive in('true','True',1,'1'):
			recursive = True
		else: recursive = False
		#inkex.debug(self.options.prop_value)
		for i,selnode in self.selected.iteritems():
			self.change_prop(selnode,prop,value)
			if recursive == True:
				for node in selnode.xpath('.//*', namespaces=inkex.NSS):
					self.change_prop(node,prop,value)
			#if style.has_key(prop):
			#	del style[prop]



if __name__ == '__main__':
	e = deletepropertyfromstyle()
	e.affect()