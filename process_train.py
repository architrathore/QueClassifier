# -*- coding: utf-8 -*-
import goslate

queFile = open('train_5500.label','r')
dataFile = open('translate_intermediate.label','w')
gs = goslate.Goslate()
i = 3188
for row in queFile:
	category,engQue = row.rstrip().split(' ',1)
	try:
		dataFile.write(engQue+'\n')
	except UnicodeDecodeError:
		print gs.translate(engQue, 'hi')
	i+=1
	
with open('train_intermediate.label', 'r') as f:
	quesBatch = f.read()
print quesBatch
dataFile.write((gs.translate(quesBatch,'hi')).encode('utf8'))