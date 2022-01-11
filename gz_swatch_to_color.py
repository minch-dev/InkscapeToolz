#!/usr/bin/env python 

import inkex,simplestyle
from grabz import *

class swatchtocolor(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		if len(self.selected)>0 :
			for i,node in self.selected.iteritems():
				style = simplestyle.parseStyle(node.get('style'))
				for attrib in ['fill','stroke','color']:
					if style.has_key(attrib):
						tsvet = style[attrib]
						if(tsvet != 'none' and tsvet.startswith('url(#')):
							gradient_wrapper = self.xpathSingle( "//*[@id='%s']" % (tsvet[len('url(#'):tsvet.find(')')]) )
							if gradient_wrapper.tag != inkex.addNS('pattern','svg'):
								wrapper_href = gradient_wrapper.get(inkex.addNS("href", "xlink"))
								if(wrapper_href!=None):
									gradient = self.xpathSingle( "//*[@id='%s']" %(wrapper_href[1:]) )
								else:
									gradient = gradient_wrapper
								swatch_type = gradient.get('{http://www.openswatchbook.org/uri/2009/osb}paint')
								if swatch_type == 'solid':
									stop_style = simplestyle.parseStyle(gradient[0].get('style'))
									if stop_style['stop-opacity']!=None:
										style[attrib+'-opacity'] = stop_style['stop-opacity']
									if stop_style['stop-color']!=None:
										style[attrib] = stop_style['stop-color']

				node.set('style', simplestyle.formatStyle(style))

if __name__ == '__main__':
	e = swatchtocolor()
	e.affect()