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

def run_this(command):
	if bsubprocess:
		p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
		return_code = p.wait()
		pf = p.stdout
		err = p.stderr
	else:
		_, pf, err = os.open3(command)
	pf.close()

def escape_quotes(s):
	return s.replace("'","\\'").replace('"','\\"')
def escape_double(s):
	return s.replace('"','\\"')
def escape_slashes(s):
	return s.replace('\\','\\\\')
def fake_double(s):
	return s.replace('"',"''").replace('?','{o_O}')

def randomize(keywords,cap,exclude=set()):
	if cap < 1:
		return []
	randomized = list([k for k in keywords if k not in exclude ])
	total = len(randomized)
	if total<cap:
		cap = total
	kk = total-1
	while (total>cap):
		if(kk <8):
			kk = total-1
		chance = float(kk)/(float(total)*1.8)
		if(chance < 0.25):
			chance = 0.25
		coin = random.random()
		if coin<chance:
			del randomized[kk]
		kk-=1
		total = len(randomized)
	return randomized

remove_words_set = (['',' ','a','an','the','is','are','he','she','it','his','her','its','s','as','of','and','or','with','w','without','wo','w/o','no','than','then','there','to','your','for','if','up','down','out','in','on','off','away'])
def get_words(sample_string):
	global remove_words_set
	sample_string = sample_string.replace(',',' ').replace(';',' ').replace('&',' ').replace('"',' ').replace('!',' ').replace('?',' ').replace(':',' ').replace('.',' ').replace("'",' ')
	sample_list = [sw.strip() for sw in sample_string.split(' ')]
	sample_list = [w for w in sample_list if w not in remove_words_set ]
	sample_set = set(sample_list)
	return sample_set
inkex.localize()

locale.setlocale(locale.LC_ALL, '')

class cutit(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		#need a popup with settings, but fuck it
		collection_mode = False
		per_row = 2
		per_col = 2
		src = self.document.getroot()
		modified = copy.deepcopy(src)
		#unlink clones
        #list index out of range
		# for clone in modified.xpath('//svg:use', namespaces=inkex.NSS):
			# Grabz.unlinkClone(self,clone,True)
		
		
		base_titles_start = []
		base_titles_start_layer = modified.xpath('//svg:g[@inkscape:label="base_titles_start"]', namespaces=inkex.NSS)
		if base_titles_start_layer!=None and base_titles_start_layer!=[]:
			base_titles_start_layer = base_titles_start_layer[0]
			base_titles_start_txts = base_titles_start_layer.xpath('svg:text/svg:tspan', namespaces=inkex.NSS)
			if base_titles_start_txts!=None and base_titles_start_txts!=[]:
				for bs in base_titles_start_txts:
					base_titles_start.append( [bs.text,get_words(bs.text)] )
			base_titles_start_layer.getparent().remove(base_titles_start_layer)
		
		base_titles = []
		base_titles_layer = modified.xpath('//svg:g[@inkscape:label="base_titles"]', namespaces=inkex.NSS)
		if base_titles_layer!=None and base_titles_layer!=[]:
			base_titles_layer = base_titles_layer[0]
			base_titles_txts = base_titles_layer.xpath('svg:text/svg:tspan', namespaces=inkex.NSS)
			if base_titles_txts!=None and base_titles_txts!=[]:
				for b in base_titles_txts:
					base_titles.append( [b.text,get_words(b.text)] )
			base_titles_layer.getparent().remove(base_titles_layer)
		
		base_keywords = ''
		base_keywords_layer = modified.xpath('//svg:g[@inkscape:label="base_keywords"]', namespaces=inkex.NSS)
		if base_keywords_layer!=None and base_keywords_layer!=[]:
			base_keywords_layer = base_keywords_layer[0]
			base_keywords_txt = base_keywords_layer.xpath('svg:text/svg:tspan', namespaces=inkex.NSS)
			if base_keywords_txt!=None and base_keywords_txt!=[]:	
				base_keywords = base_keywords_txt[0].text
			base_keywords_layer.getparent().remove(base_keywords_layer)
		base_keywords = [k.strip() for k in base_keywords.split(',') if k !='']	

		russian_layer = modified.xpath('//svg:g[@inkscape:label="russian"]', namespaces=inkex.NSS)
		if russian_layer!=None and russian_layer!=[]:
			russian_layer = russian_layer[0]
			russian_layer.getparent().remove(russian_layer)
		
		#convert text, stars etc?
		#convert objects to paths including clones
		#!!!squarez R open
		#!!!no love for ellipses
		#for node in modified.xpath('//svg:g[@inkscape:groupmode="layer"][@inkscape:label!="ids"]//*[not(self::svg:g)]', namespaces=inkex.NSS):
		#	Grabz.objectToPath(self,node,True)
		#group ungrouped elements
		for object in modified.xpath('//svg:g[@inkscape:groupmode="layer"][@inkscape:label!="ids"][@inkscape:label!="titles"][@inkscape:label!="keywords"]/*[not(self::svg:g)]', namespaces=inkex.NSS):
			group_node = inkex.etree.Element(inkex.addNS('g','svg'))
			parent=object.getparent()
			parent.insert(parent.index(object),group_node)
			group_node.append(object)
		grid = src.xpath('//inkscape:grid', namespaces=inkex.NSS)[0]
		#from document grid
		width = int(self.unittouu(grid.get('spacingx')))
		height = int(self.unittouu(grid.get('spacingy')))
		#no idea where to get it
		save_path = 'Z:/export/'
		image_magic = 'A:/Programs/ImageMagick-7.0.5-4-portable-Q16-x86/convertz.exe'
		exif_tool = 'A:/Programs/exiftool106.exe'
		author = 'shutterstock.com/g/Ta-nya'
		doc_width = int(self.unittouu(src.get('width')))
		doc_height = int(self.unittouu(src.get('height')))
		if collection_mode == True:
			width = width * per_row
			height = height * per_col
		if width > height:
			export_width  = width
			export_dpi_ = float(export_width)/float(width)
			export_height = int(export_dpi_*height)
			export_dpi = export_dpi_ * 90
		else:
			export_height = height
			export_dpi_ = float(export_height)/float(height)
			export_width  = int(export_dpi_*width)
			export_dpi = export_dpi_ * 90
		#inkex.debug('export_width=%s export_height=%s width=%s height=%s dpiminus90=%s' % (export_width,export_height,width,height,export_dpi_))
		width_px = str(width)+'px'
		height_px = str(height)+'px'
		count = 0
		view = modified.xpath('//sodipodi:namedview', namespaces=inkex.NSS)[0]
		view.set('zoom', "1")
		view.set(inkex.addNS('zoom','inkscape'), "1")
		view.set(inkex.addNS('cx','inkscape'), str(width/2))
		view.set(inkex.addNS('cy','inkscape'), str(height/2))
		modified.set(inkex.addNS('export-xdpi','inkscape'), str(export_dpi))
		modified.set(inkex.addNS('export-ydpi','inkscape'), str(export_dpi))
		modified.set('width',width_px)
		modified.set('height',height_px)
		group_filename = src.get(inkex.addNS('docname','sodipodi')).replace('.svg', '');
		
		for y0  in range(0,doc_height,height):
			for x0 in range(0,doc_width,width):
				count+=1
				x1 = x0 + width
				y1 = y0 + height
				cutname = str(count)
				#--
				cut = copy.deepcopy(modified)
				for object in cut.xpath('//svg:g[@inkscape:groupmode="layer"]/*', namespaces=inkex.NSS):
					xxyy = computeBBox(object)
					if xxyy == None:
						inkex.debug(object)
						object.getparent().remove(object)
					elif int(xxyy[0])<x0-1 or int(xxyy[1])>x1+1 or int(xxyy[2])<y0-1 or int(xxyy[3])>y1+1 :
						object.getparent().remove(object)
				for layer in cut.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS):
					layer.set( 'transform','translate(%f,%f)' %(-x0,-y0) )
				
				id_layer = cut.xpath('//svg:g[@inkscape:label="ids"]', namespaces=inkex.NSS)[0]
				if id_layer!=None:
					id_txt = cut.xpath('//svg:g[@inkscape:label="ids"]//svg:tspan', namespaces=inkex.NSS)
					if id_txt!=None and id_txt!=[]:
						cutname = ""
						total_i = len(id_txt)
						
						for i in range(0,total_i,1):
							part = id_txt[i].text
							if part != None:
								if i!=0 and i==total_i-1:
									cutname += ' & '
								elif i>0:
									cutname += ', '
								cutname += id_txt[i].text
					else: continue
					id_layer.getparent().remove(id_layer)
				else: continue
				
				title = ""
				title_layer = cut.xpath('//svg:g[@inkscape:label="titles"]', namespaces=inkex.NSS)
				if title_layer!=None and title_layer!=[]:
					title_layer = title_layer[0]
					if collection_mode == True:
						title = "A set of emoji icons consisting of "+cutname+" emoticons"
					else:
						title_txt = cut.xpath('//svg:g[@inkscape:label="titles"]//svg:tspan', namespaces=inkex.NSS)
						if title_txt!=None and title_txt!=[]:	
							title = title_txt[0].text
							if title == None:
								title = title_txt[1].text
					title_layer.getparent().remove(title_layer)
				title = base_titles_start[0][0] + title
				#randomize IT
				title = title.replace('  ',' ')
				title_words = get_words(title)

				for part_title,part_words in base_titles:
					repeats = title_words & part_words
					if (len(repeats) == 0):
						temp_title = title + part_title
						if(len(temp_title)<201):
							title = temp_title
							title_words |= part_words
				title = escape_double(title)
					
				keywords = []
				keywords_layer = cut.xpath('//svg:g[@inkscape:label="keywords"]', namespaces=inkex.NSS)
				if keywords_layer!=None and keywords_layer!=[]:
					keywords_layer = keywords_layer[0]
					keywords_txt = cut.xpath('//svg:g[@inkscape:label="keywords"]//svg:tspan', namespaces=inkex.NSS)
					if keywords_txt!=None and keywords_txt!=[]:
						keyword_sets = []
						keywords_max_length = 0
						for k in range(0,len(keywords_txt),1):
							if keywords_txt[k].text==None:
								continue
							keyword_sets.append( [kk.strip() for kk in keywords_txt[k].text.split(',') if kk !=''] )
							new_len = len(keyword_sets[k])
							if new_len > keywords_max_length:
								keywords_max_length = new_len
						for ki in range (0,keywords_max_length,1):
							for ks in range (0,len(keyword_sets),1):
								if ki < len(keyword_sets[ks]):
									key = keyword_sets[ks][ki]
									if key not in keywords:
										keywords.append(key)
					keywords_layer.getparent().remove(keywords_layer)
				random_keys = randomize(base_keywords,50-len(keywords),keywords)
				keywords = escape_double(','.join(keywords + random_keys))
				
				filename = '%s %s' % (group_filename,cutname)
				png_path = fake_double(save_path+filename+'.png')
				jpg_path = fake_double(save_path+filename+'.jpg')
				svg_path = fake_double(save_path+filename+'.svg')
				cut.set(inkex.addNS('docname','sodipodi'), filename+'.svg')
				cut.set(inkex.addNS('export-filename','inkscape'), '.\\'+filename+'.png')
				cut.set('viewBox', '0 0 '+str(width)+' '+str(height))
				
				svg_string = inkex.etree.tostring(cut)
				cf = open(svg_path, 'w+')
				cf.write(svg_string)
				cf.close()
				run_this('inkscape "%s" --export-png="%s" -w%d -h%d' % (svg_path,png_path,export_width,export_height))
				run_this('%s -units PixelsPerInch "%s" -quality 100 -density 300 "%s"' % (image_magic,png_path,jpg_path))
				run_this('%s -XMP-dc:creator="%s" -IPTC:By-line="%s"     -XMP-dc:identifier="%s" -IPTC:ObjectName="%s"    -XMP-dc:title="%s" -IPTC:Caption-Abstract="%s"     -XMP-dc:subject="%s" -sep "," -IPTC:Keywords="%s" -overwrite_original "%s"' % (exif_tool,author,author,filename,filename,title,title,keywords,keywords,jpg_path))
		
	def get_localised_string(self, str):
		return locale.format("%.f", float(str), 0)
		
if __name__ == '__main__':
	e = cutit()
	e.affect()

