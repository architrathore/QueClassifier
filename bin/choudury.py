# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import defaultdict
import sys, codecs
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

C 	=	1	#	consonant
CV	=	2	#	consonant-vowel
V 	=	3	#	full vowel
CH 	=	4	#	consonant-halant

ERROR		=	0
VYANJAN 	= 	1
SWAR 		= 	2
MATRA 		= 	3
HALANT 		= 	4

syllables = []

vyanjan = 	(	'क','ख','ग','घ','ङ',	\
				'च','छ','ज','झ','ञ',	\
				'ट','ठ','ड','ढ','ण',		\
				'त','थ','द','ध','न',		\
				'प','फ','ब','भ','म',		\
				'य','र','ल','व',			\
				'श','ष','स','ह',			\
				'क़','ख़','ग़','ज़',		\
				'ड़','ढ़','फ़','य़',		\
				'ऩ'						)
swar =	(	'अ','आ',	\
			'इ','ई',		\
			'उ','ऊ',	\
			'ए',	'ऐ',		\
			'ओ','औ'		\
			'ऑ'			)
matra =	(	'ा',		\
			'ि','ी',	\
			'ु','ू',	\
			'े','ै',	\
			'ो','ौ',	\
			'ॉ','ं'	\
			'़','ृ',	\
			'ॄ'			)
halant = (	'्'			)

devnagri_latin_map = {
	'क':	'ka',	'ख':	'kha',	'ग':		'ga',	'घ':	'gha',	'ङ':	'na',
	'च':	'cha',	'छ':	'cha',	'ज':	'ja',	'झ':	'jha',	'ञ':	'jna',
	'ट':	'ta',	'ठ':		'tha',	'ड':	'da',	'ढ':		'dha',	'ण':	'na',
	'त':	'ta',	'थ':	'th',	'द':		'da',	'ध':	'dha',	'न':	'na',
	'प':		'pa',	'फ':	'fa',	'ब':		'ba',	'भ':	'bha',	'म':		'ma',
	'य':		'ya',	'र':		'ra',	'ल':	'la',	'ळ':	'la',	'व':		'va',
	'श':	'sha',	'ष':		'sha',	'स':	'sa',	'ह':		'ha',
	'क़':	'qa',	'ख़':	'kha',	'ग़':		'ga',	'ज़':	'za',
	'ड़':	'ra',	'ढ़':		'rha',	'फ़':	'fa',	
	'अ':	'a',	'आ':	'aa',	'इ':		'i',	'ई':		'i',	'उ':	'u',	'ऊ':	'u',	'ए':		'e',	'ऐ':		'ae',	'ओ':	'o',	'औ':	'au', 'ऑ':	'o',
	'ऋ':	'ri',	'ऌ':	'lra',	'ॠ':	'ra',	'ॡ':	'lra',
	'क्ष':	'ksha',	'त्र':	'tra',	'ज्ञ':	'jna',
	'ं':	'n',	'ः':	'h',	'ँ':	'n',
	'ा':	'aa',	'ि':	'i',	'ी':	'i',	'ु':	'u',	'ू':	'u',	'े':	'e',	'ै':	'ai',	'ो':	'o',	'ौ':	'au',
	'ृ':	'ri',	'ॢ':	'lr',	'ॄ':	'r',	'ॣ':	'lr',
	'~':	''	,	'्':	''
}
# devnagri_latin_map = {k.decode('utf8'): v.decode('utf8') for k, v in devnagri_latin_map.items()}

def printSuchhi(suchhi):
	unicode_list = repr([x.encode(sys.stdout.encoding) for x in suchhi]).decode('string-escape')
	print unicode_list

def aksharaPrakaar(akshara):
	if akshara in vyanjan:
		return VYANJAN
	elif akshara in swar:
		return SWAR
	elif akshara in matra:
		return MATRA
	elif akshara in halant:
		return HALANT
	else: 
		return ERROR

def sanyuktPrakaar(sanyukt_shabd):
	if len(sanyukt_shabd) == 2:
		first_prakaar = aksharaPrakaar(sanyukt_shabd[0])
		second_prakaar = aksharaPrakaar(sanyukt_shabd[1])
		if first_prakaar == VYANJAN and second_prakaar == MATRA:
			return CV
		elif first_prakaar == VYANJAN and second_prakaar == HALANT:
			return CH
	elif len(sanyukt_shabd) == 1:
		prakaar = aksharaPrakaar(sanyukt_shabd)
		if prakaar == SWAR:
			return V
		elif prakaar == VYANJAN:
			return C
	return ERROR

def createShabdSuchhi(shabd):
	suchhi = []
	if len(shabd) == 1:
		suchhi.append(shabd[0])
	elif len(shabd) == 2:
		if aksharaPrakaar(shabd[0]) == VYANJAN and aksharaPrakaar(shabd[1]) == MATRA:
			suchhi.append(shabd[0]+shabd[1])
		else:
			suchhi.append(shabd[0])
			suchhi.append(shabd[1])
	else:
		i = 0
		for i in range(len(shabd)-1):
			akshara = shabd[i]
			next_akshara = shabd[i+1]
			prakaar = aksharaPrakaar(akshara)
			next_prakaar = aksharaPrakaar(next_akshara)
			if prakaar == ERROR:
				# print "Error: invalid character in input word"
				suchhi = []
				break
			elif prakaar == VYANJAN and next_prakaar == SWAR:
				suchhi.append(akshara)
			elif prakaar == VYANJAN and next_prakaar == VYANJAN:
				suchhi.append(akshara)
			elif prakaar == SWAR:
				suchhi.append(akshara)
			elif prakaar == VYANJAN and next_prakaar == HALANT:
				suchhi.append(akshara+next_akshara)
				i += 1
			elif prakaar == VYANJAN and next_prakaar == MATRA:
				suchhi.append(akshara+next_akshara)
				i += 1
		if i == len(shabd)-2:
			suchhi.append(shabd[i+1])
	return suchhi

def findConjugatePos(shabd):
	conj_pos = {}
	x=0
	while x < shabd.length:
		start_pos = x
		if x+1 < shabd.length and sanyuktPrakaar(shabd.suchhi[x]) == CH and sanyuktPrakaar(shabd.suchhi[x+1]) in (C,CV):
			conj_pos[start_pos] = shabd.suchhi[x] + shabd.suchhi[x+1]
			x+=1
		elif x+2 < shabd.length and sanyuktPrakaar(shabd.suchhi[x]) == CH and sanyuktPrakaar(shabd.suchhi[x+1]) == CH and sanyuktPrakaar(shabd.suchhi[x+2]) in (C,CV):
			conj_pos[start_pos] = shabd.suchhi[x] + shabd.suchhi[x+1] + shabd.suchhi[x+2]
			x+=2
		x+=1
	return conj_pos

class ShabdClass:
	def __init__(self,suchhi):
		self.suchhi = suchhi
		self.length = len(self.suchhi)
		self.sound_suchhi = ['U']*self.length
		self.syllable_break = ['']*self.length

	def printShabd(self):
		printSuchhi(self.suchhi)
		printSuchhi(self.sound_suchhi)
		printSuchhi(self.syllable_break)

	def rule1(self):
		for x in range(self.length):
			if sanyuktPrakaar(suchhi[x]) in (CV,V):
				self.sound_suchhi[x] = 'F'
			elif sanyuktPrakaar(suchhi[x]) == CH:
				self.sound_suchhi[x] = 'H'

	def rule2(self):
		for x in range(self.length):
			curr = suchhi[x]
			if x > 0 and curr == 'य':
				prev = suchhi[x-1]
				if prev[-1] in ('ि','ी','ु','ू',) or prev == 'रि':
					self.sound_suchhi[x] = 'F'

	def rule3(self):
		for x in range(self.length):
			curr = suchhi[x]
			if x > 0 and curr in ('य','र','ल','व'):
				if self.sound_suchhi[x] == 'U' and self.sound_suchhi[x-1] == 'H':
					self.sound_suchhi[x] = 'F'
	def rule4(self):
		for x in range(self.length-1):
			if x < (self.length-1) and sanyuktPrakaar(self.suchhi[x]) == C and self.sound_suchhi[x] == 'U' and sanyuktPrakaar(self.suchhi[x+1]) == V:
				self.sound_suchhi[x] = 'F'

	def rule5(self):
		x = 0
		flag = False
		while x < shabd.length and shabd.length > 1:
			flag = (shabd.sound_suchhi[0] == 'U')
			if flag and sanyuktPrakaar(shabd.suchhi[0]) == C and shabd.sound_suchhi[1] == 'F':
				shabd.sound_suchhi[0] = 'F'
			x += 1
			return

	def rule6(self):
		if sanyuktPrakaar(self.suchhi[-1]) == C and self.sound_suchhi[-1] == 'U': 
			self.sound_suchhi[-1] = 'H'

	def rule7(self):
		for x in range(self.length-1):
			if sanyuktPrakaar(self.suchhi[x]) == C and self.sound_suchhi[x] == 'U' and self.suchhi[x+1] == C and self.sound_suchhi[x+1] == 'H':
				self.sound_suchhi[x] = 'F'

	def rule8(self):
		for x in range(1,self.length-1):
			if sanyuktPrakaar(suchhi[x]) == C and self.sound_suchhi[x] == 'U':
				if self.sound_suchhi[x-1] == 'F' and (self.sound_suchhi[x+1] in ('F','U')):
					self.sound_suchhi[x] = 'H'
				else:
					self.sound_suchhi[x] = 'F'

def schwa_delete(shabd):
	shabd.rule1()
	# shabd.printShabd()
	shabd.rule2()
	# shabd.printShabd()
	shabd.rule3()
	# shabd.printShabd()
	shabd.rule4()
	# shabd.printShabd()
	shabd.rule5()
	# shabd.printShabd()
	shabd.rule6()
	# shabd.printShabd()
	shabd.rule7()
	# shabd.printShabd()
	shabd.rule8()
	# shabd.printShabd()

def checkConjLast(conj_pos,shabd):
	if conj_pos.keys():
		max_pos = max(conj_pos.keys())
		length = len(conj_pos[max(conj_pos.keys())])
		if length in (3,4):
			char_width = 2
		elif length in (5,6):
			char_width = 3
		return max_pos+char_width == shabd.length
	else:
		return False

def syllabify(shabd):
	schwa_delete(shabd)
	for x in range(shabd.length - 1):
		if shabd.sound_suchhi[x] == 'F' and shabd.sound_suchhi[x+1] == 'F' and sanyuktPrakaar(shabd.suchhi[x+1])!= V:
			shabd.syllable_break[x] = '~'
	for x in range(shabd.length - 1):
		if shabd.sound_suchhi[x] == 'H' and shabd.sound_suchhi[x+1] == 'F' and not x == 0 and not shabd.syllable_break[x-1] == '~' and not shabd.suchhi[x]+shabd.suchhi[x+1] in ('प्र','त्र'):
			shabd.syllable_break[x] = '~'
	conj_pos = findConjugatePos(shabd)
	for x in conj_pos.keys():
		if not checkConjLast(conj_pos, shabd) and not shabd.suchhi[x]+shabd.suchhi[x+1] in ('प्र','त्र'):
			shabd.syllable_break[x] = '~'

def printSyllabified(shabd):
	sys.stdout.write(''.join("%s%s" %t for t in zip(shabd.suchhi,shabd.syllable_break)))
	# for x in range(shabd.length):
		# sys.stdout.write(shabd.suchhi[x])
		# print shabd.suchhi[x],
		# sys.stdout.write(shabd.syllable_break[x])
		# print shabd.syllable_break[x],
	# out_file.write('~')
	# print '~'

# f = open('corpus.txt', 'r')
# devnagri_chars = list(vyanjan) + list(swar) + list(matra) + list(halant)
# words = []
# for line in f:
# 	word = ""	
# 	line  = line.decode('utf-8')
# 	for character in line:
# 		if character in devnagri_chars:
# 			word += character
# 		else:
# 			if(len(word)):
# 				words.append(word)
# 				word = ""
# 	if len(word):
# 		words.append(word)
# print words
# out_file = codecs.open("choudury_temp.out","w","utf_8")
# shabd_list = []
# for input_shabd in words:
# 	suchhi = createShabdSuchhi(input_shabd)
# 	if suchhi:
# 		shabd = ShabdClass(suchhi)
# 		syllabify(shabd)
# 		shabd_list.append(shabd)
# 		printSyllabified(shabd)

# inp_str = raw_input()
# inp_str = inp_str.decode('utf-8')
# words = []
# word = ""
# devnagri_chars = list(vyanjan) + list(swar) + list(matra) + list(halant)
# for character in inp_str:
# 	if character in devnagri_chars:
# 		word += character
# 	else:
# 		if(len(word)):
# 			words.append(word)
# 			word = ""
# if len(word):
# 	words.append(word)
# # print words
# shabd_list = []
# for input_shabd in words:
# 	suchhi = createShabdSuchhi(input_shabd)
# 	if suchhi:
# 		shabd = ShabdClass(suchhi)
# 		# shabd.printShabd()
# 		syllabify(shabd)
# 		# shabd.printShabd()
# 		# shabd_list.append(shabd)
# 		printSyllabified(shabd)
# 		print ' ',
def validateChar(char):
	if char not in devnagri_latin_map.keys()+[' ']:
		return ''
	return char

def charContext(s,i):
	if i > 1 and i < len(s)-2:
		return validateChar(s[i-2]),validateChar(s[i-1]),validateChar(s[i]),validateChar(s[i+1]),validateChar(s[i+2])
	elif i == 1:
		return '',validateChar(s[i-1]),validateChar(s[i]),validateChar(s[i+1]),validateChar(s[i+2])
	elif i == 0:
		return '','',validateChar(s[i]),validateChar(s[i+1]),validateChar(s[i+2])
	elif i == len(s)-2:
		return validateChar(s[i-2]),validateChar(s[i-1]),validateChar(s[i]),validateChar(s[i+1]),''
	elif i == len(s)-1:
		return validateChar(s[i-2]),validateChar(s[i-1]),validateChar(s[i]),'',''

def transliterate(context_tuple):
	prev2 = context_tuple[0]
	prev1 = context_tuple[1]
	curr = context_tuple[2]
	next1 = context_tuple[3]
	next2 = context_tuple[4]
	# sys.stdout.write(prev2)
	# sys.stdout.write(prev1)
	# sys.stdout.write(curr)
	# sys.stdout.write(next1)
	# sys.stdout.write(next2)
	# print 
	# print curr+":"
	if (curr == 'ं'):
		if (prev1 in ['स']):
			sys.stdout.write('m')
		elif(prev2+prev1 == 'मे'):
			sys.stdout.write('in')
		else:
			sys.stdout.write(devnagri_latin_map[curr])
	elif(curr == 'ए' and prev1 in ['ि','ी']+list(swar)+list(vyanjan)):
			sys.stdout.write('ye')
	elif(curr == 'य' and next1 == ' '):
		sys.stdout.write('ya')
	elif(curr in list(vyanjan) and next1 in list(matra)+['्',' ']):
		sys.stdout.write(devnagri_latin_map[curr].replace('a',''))
	elif(curr in ['आ','ा'] and next1 in [' ','']):
		sys.stdout.write('a')
	else:
		sys.stdout.write(devnagri_latin_map[curr])

inp_str = raw_input()
inp_str = inp_str.decode('utf-8')
words = []
outstr = ""
hindi_word = ""
devnagri_chars = list(vyanjan) + list(swar) + list(matra) + list(halant)
for character in  inp_str:
	if character not in devnagri_chars:
		suchhi = createShabdSuchhi(hindi_word)
		if suchhi:
			shabd = ShabdClass(suchhi)
			syllabify(shabd)
			# shabd.printShabd()
			# printSyllabified(shabd)
			outstr += ''.join("%s%s" %t for t in zip(shabd.suchhi,shabd.syllable_break))
		# print hindi_word,
		hindi_word = ""
		# sys.stdout.write(character)
		outstr += character
	else:
		hindi_word += character
outstr += hindi_word
print inp_str
print outstr
print len(outstr)
for i,character in zip(xrange(len(outstr)),outstr):
	# print i,character
	if character in devnagri_latin_map:
		# if (i < len(outstr)-1) and (outstr[i+1] in list(matra) or outstr[i+1] in ['~',' ','"','\'','्']) and (outstr[i] not in list(matra) or outstr[i] not in list(swar)):
		# 	sys.stdout.write(devnagri_latin_map[character].replace('a',''))
		# else:
		# 	sys.stdout.write(devnagri_latin_map[character])
		# print "char "+str(i),
		# print character+'	:	',
		# print charContext(outstr,i)
		transliterate(charContext(outstr,i))
	# if character in devnagri_latin_map:
	# 	sys.stdout.write(devnagri_latin_map[character])
	else:
		sys.stdout.write(character)
print 