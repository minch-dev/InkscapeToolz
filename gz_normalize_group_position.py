#!/usr/bin/env python
import inkex
import re,string,simplepath,simplestyle
from grabz import *
trans_pattern = re.compile('translate\(([-0-9\.]+),([-0-9\.]+)\)')
matrix_pattern = re.compile('matrix\(([-0-9\.\,]+)\)')

class normalizeit(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		global trans_pattern
		if len(self.selected)>0:
			for i,grp in self.selected.iteritems():
				if node.tag == inkex.addNS('g','svg'):
					xxyy = computeBBox([grp])
					
					real_pos_x = float(xxyy[0])
					real_pos_y = float(xxyy[2])
					tran_pos_x = 0.0
					tran_pos_y = 0.0
					transform = grp.get('transform')
					if transform != None:
						translate = trans_pattern.match(transform)
						if translate != None:
							tran_pos_x = float(translate.group(1))
							tran_pos_y = float(translate.group(2))
					delta_pos_x = tran_pos_x - real_pos_x
					delta_pos_y = tran_pos_y - real_pos_y
					# inkex.debug((real_pos_x,real_pos_y))
					# inkex.debug((tran_pos_x,tran_pos_y))
					# inkex.debug((delta_pos_x,delta_pos_y))
					if not(delta_pos_x==0 and delta_pos_y==0):
						for node in grp.xpath('./*', namespaces=inkex.NSS):
							node_transform = node.get('transform')
							if node_transform == None:
								node_transform = ''
							node.set('transform', 'translate(%f,%f) ' % (delta_pos_x,delta_pos_y) +node_transform)
						grp.set('transform','translate(%f,%f)' % (real_pos_x,real_pos_y) )

if __name__ == '__main__':
	e = normalizeit()
	e.affect()

