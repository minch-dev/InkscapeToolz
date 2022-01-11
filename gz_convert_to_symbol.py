#!/usr/bin/env python
import re,inkex
import os
import sys
import locale
import random
try:
	from subprocess import Popen, PIPE
	bsubprocess = True
except:
	bsubprocess = False
from grabz import *
from simpletransform import *

def insert_after(element,new_element):
	parent = element.getparent()
	parent.insert(parent.index(element)+1, new_element)

class cutit(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		collection_mode = False
		default_pos_x = 0.0 #-25000.0
		default_pos_y = 0.0 #30000.0
		src = self.document.getroot()

		doc_width = int(self.unittouu(src.get('width')))
		doc_height = int(self.unittouu(src.get('height')))
		
		if len(self.selected)==1 :
			gr = self.selected.values()[0]
			xxyy = computeBBox(self.selected.values())
			translate_x = xxyy[0]-default_pos_x
			translate_y = xxyy[2]-default_pos_y
			gr.set('transform','translate(%f,%f)' % (-translate_x,-translate_y) )
			clone = inkex.etree.Element('use')
			clone.set( 'transform', 'translate(%f,%f)' % (translate_x,translate_y) )
			clone.set(  inkex.addNS('href','xlink'), '#%s' % gr.get('id') )
			insert_after(gr,clone)
			#inkex.debug((translate_x,translate_y))
			
		#unlink clones
        #list index out of range
		# for clone in modified.xpath('//svg:use', namespaces=inkex.NSS):
			# Grabz.unlinkClone(self,clone,True)
		#convert text, stars etc?
		#convert objects to paths including clones
		#!!!squarez R open
		#!!!no love for ellipses
		#for node in modified.xpath('//svg:g[@inkscape:groupmode="layer"][@inkscape:label!="ids"]//*[not(self::svg:g)]', namespaces=inkex.NSS):
		#	Grabz.objectToPath(self,node,True)
		#group ungrouped elements
		
if __name__ == '__main__':
	e = cutit()
	e.affect()

