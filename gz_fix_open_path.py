#!/usr/bin/env python 
'''
select open paths
'''
import inkex
import math,re,simplepath,cubicsuperpath


class Lust(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		svg = self.document.getroot()
		if len(self.selected)<=0 :
			for p in svg.xpath('//svg:path', namespaces=inkex.NSS):
				#if self.check_open(p):
				self.close_harder(p)
		else :
			for i,p in self.selected.iteritems():
				#if self.check_open(p):
				self.close_harder(p)

	def check_open(self,p):
		open = True
		str = p.get('d')
		r = re.compile('.+[zZ].*$')
		if(re.search(r, str)) :
			open = False
		return open
		
	def close_open(self,p):
		p.set('d', p.get('d')+' z')

	def close_harder(self,p):
		d = p.get('d')
		d = simplepath.formatPath( simplepath.parsePath(d) )
		d = re.sub(r'(?i)(m[^mz]+)',r'\1 Z ',d)
		d = re.sub(r'(?i)\s*z\s*z\s*',r' Z ',d)
		p.set('d', d)
if __name__ == '__main__':
	e = Lust()
	e.affect()


