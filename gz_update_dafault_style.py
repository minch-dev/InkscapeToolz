#!/usr/bin/env python 
import inkex

class updatedefaultstyle(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		root = self.document.getroot()
		style_string = root.get('style')
		for layer in root.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS):
			layer.set('style',style_string)

if __name__ == '__main__':
	e = updatedefaultstyle()
	e.affect()