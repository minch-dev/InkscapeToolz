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


def escape_quotes(s):
	return s.replace("'","\\'").replace('"','\\"')
def escape_double(s):
	return s.replace('"','\\"')
def escape_slashes(s):
	return s.replace('\\','\\\\')
def fake_double(s):
	return s.replace('"',"''").replace('?','{o_O}')
	

def randomize(keywords,cap,exclude=set()):
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
	return sample_list
inkex.localize()

locale.setlocale(locale.LC_ALL, '')

class cutit(Grabz):
	def __init__(self):
		inkex.Effect.__init__(self)

	def effect(self):
		debug = True
		base_keywords = ',2018,merry,christmas,coffee,xmas,hot,chocolate,cup,cocoa,mug,vector,winter,tea,background,holiday,drink,cartoon,breakfast,illustration,design,warm,food,cute,card,snow,cozy,cosy,happy,cacao,latte,aroma,quote,dessert,funny,morning,break,smoke,drawing,steam,red,cappuccino,snowflake,text,coffe,day,beverage,greeting,character,creative,hand drawn,new year,ugly,flake,art,symbol,glass,abstract,traditional,fun,adorable,noel,white,green,celebration,typography,teacup,mockup,festive,espresso,flavor,vacation,vapour,vapor,element,decoration,postcard,carton,clipart,sweet,seasonal,print,chrismas,cristmas,'
		base_keywords = [k.strip() for k in base_keywords.split(',') if k !='']	
		keywords = 'brown,red,deer,reindeer,handle,bean,antlers,horns,heart,picture,'
		keywords = [k.strip() for k in keywords.split(',') if k !='']
		
		keys_to_add = 49-len(keywords)
		random_keys = randomize(base_keywords,keys_to_add,keywords)
		
		keywords = escape_double(','.join(keywords + random_keys))
		inkex.debug(keywords)
				

		
	def get_localised_string(self, str):
		return locale.format("%.f", float(str), 0)
		
if __name__ == '__main__':
	e = cutit()
	e.affect()

