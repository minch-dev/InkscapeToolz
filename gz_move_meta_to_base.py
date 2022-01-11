#!/usr/bin/env python 

import inkex
from grabz import *

class metatobase(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		if len(self.selected)>0 :
			for i,grp in self.selected.iteritems():
				grp_id = grp.get('id')
				meta_base = grp.xpath('.//*[@meta_base]', namespaces=inkex.NSS)[0]
				meta_name = grp.get('meta_name')
				meta_title = grp.get('meta_title')
				meta_keywords = grp.get('meta_keywords')
				if meta_name!='' and meta_name!=None:
					meta_base.set(	'meta_name', meta_name)
					grp.set('meta_name','')
				else:
					inkex.debug(grp_id+' no name')
				if meta_title!='' and meta_title!=None:
					meta_base.set(	'meta_title', meta_title)
					grp.set('meta_title','')
				else:
					inkex.debug(grp_id+' no title')
				if meta_keywords!='' and meta_keywords!=None:
					meta_base.set(	'meta_keywords', meta_keywords)
					grp.set('meta_keywords','')
				else:
					inkex.debug(grp_id+' no keywords')
				

if __name__ == '__main__':
	e = metatobase()
	e.affect()