#!/usr/bin/env python 
'''
delete effects
'''
import inkex
class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		#inkscape:path-effect
		debug = True
		svg = self.document.getroot()
		if len(self.selected)<=0 :
			for p in svg.xpath('//*[@inkscape:path-effect]', namespaces=inkex.NSS):
				p.set(inkex.addNS('path-effect', 'inkscape'),'')
		else :
			for i,p in self.selected.iteritems():
				p.set(inkex.addNS('path-effect', 'inkscape'),'')


if __name__ == '__main__':
	e = Lust()
	e.affect()


