# -*- coding: utf-8 -*-
import goslate
import urllib2

# proxy_handler = urllib2.ProxyHandler({"http" : "http://archit:uncrack@ironport2.iitk.ac.in:3028"})
# proxy_opener = urllib2.build_opener(urllib2.HTTPHandler(proxy_handler),
#                                     urllib2.HTTPSHandler(proxy_handler))


queFile = open('train_5500.label','r')
dataFile = open('translated_test.label','w')
gs = goslate.Goslate()
i = 1
for row in queFile:
	category,engQue = row.rstrip().split(' ',1)
	try:
		dataFile.write((str(i)+"#1 "+category+" "+engQue+'\n').encode('utf8'))
		dataFile.write((str(i)+"#2 "+category+" "+gs.translate(engQue, 'hi')+'\n').encode('utf8'))
	except UnicodeDecodeError:
		print gs.translate(engQue, 'hi')
	i+=1
	
