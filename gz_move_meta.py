#!/usr/bin/env python
import re,inkex
from grabz import *


class cutit(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		if len(self.selected)>0 :
			for i,grp in self.selected.iteritems():
				
				meta_name = ''
				meta_title = ''
				meta_keywords = ''
				txt = ''
				for tspan_tag in grp.xpath('.//svg:tspan', namespaces=inkex.NSS):
					txt = tspan_tag.text
					if txt!=None and txt!=[] and txt!='':
						text_tag = tspan_tag.getparent()
						if text_tag.get('is_title') != None:
							meta_title = txt
						elif text_tag.get('is_keywords') != None:
							meta_keywords = txt
						elif text_tag.get('is_id') != None:
							meta_name = txt
						text_tag.getparent().remove(text_tag)
				if meta_name != '':
					grp.set('meta_name',meta_name)
					#refined_id = meta_name.replace('"','').replace("'",'').replace('#','').replace('.','').replace('&','').replace('-','').replace(':','').replace(',', '_').replace(';','_').replace(' ', '_').replace('!', '_exlm_').replace('?', '_qstn_').replace('__', '_').replace('__', '_').replace('__', '_').lower()
					#refined_id = 'pic_'+refined_id
					#grp.set('id',refined_id)
				if meta_title != '':
					grp.set('meta_title',meta_title)
				if meta_keywords != '':
					grp.set('meta_keywords',meta_keywords)
		
if __name__ == '__main__':
	e = cutit()
	e.affect()

