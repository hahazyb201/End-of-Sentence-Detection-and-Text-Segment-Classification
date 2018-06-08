import re
import sys
program_name = sys.argv[0]
file_name=sys.argv[1]

fo=open("data.arff","w")

print >> fo, "@RELATION CATEGORY";	
print >> fo, "@ATTRIBUTE class   {NNHEAD,QUOTED,SIG,#BLANK#,TABLE,GRAPHIC,HEADL,ADDRESS,ITEM,PTEXT}";
print >> fo, "@ATTRIBUTE blockLen   NUMERIC";	#number of lines in the block
print >> fo, "@ATTRIBUTE nnheadlikelihood   NUMERIC";	#likelihood of being NNHEAD
print >> fo, "@ATTRIBUTE quotedlikelihood   NUMERIC";	#likelihood of being QUOTED
print >> fo, "@ATTRIBUTE signatureImportant   {1,0}";	#whether the paragraph begins with '--' 
print >> fo, "@ATTRIBUTE signaturelikelihood   NUMERIC";	#likelihood of being a SIG
print >> fo, "@ATTRIBUTE graphiclikelihood   NUMERIC";	#likelihood of being a GRAPHIC
print >> fo, "@ATTRIBUTE tablelikelihood   NUMERIC";	#likelihood of being a TABLE
print >> fo, "@ATTRIBUTE addresslikelihood   NUMERIC";	#likelihood of being an ADDRESS
print >> fo, "@ATTRIBUTE itemlikelihood   NUMERIC";	#likelihood of being an ITEM


print >> fo, "@ATTRIBUTE headerEndinPeriod   {1,0}";	#whether the line ends up with a period
print >> fo, "@ATTRIBUTE headerCapitalized   NUMERIC";	#how many words are capitalized
print >> fo, "@ATTRIBUTE headerIndented   NUMERIC"; #average number of spaces or tables before the first word in a line


print >> fo, "@ATTRIBUTE wordsperline   NUMERIC";	
print >> fo, "@ATTRIBUTE blankperline   NUMERIC";	

def generateSet(file):
	fileSet=set()
	line=file.readline()
	line=line.strip('\n')
	while line:
		fileSet.add(line.lower())
		line=file.readline()
		line=line.strip('\n')
	return fileSet


Abbrevs=open("StateAbbreviations.txt",'r')

stateAbbrevs=generateSet(Abbrevs)


print >> fo, "@DATA";

data=open(file_name,'r')




def ProcessPreviousBlock(block):	
	a=nnHeadLikelihood(block)
	b=quotedLikelihood(block)
	c=signatureImportant(block)
	d=signatureLikelihood(block)
	e=graphicLikelihood(block)
	f=tableLikelihood(block)
	g=addresslikelihood(block)
	h=itemlikelihood(block)
	i=headerEndinPeriod(block)
	j=headerCapitalized(block)
	k=headerIndented(block)
	l=wordsPerLine(block)
	m=blanksPerLine(block)

	for line in block:
		out=[]
        	category=line.split()
		if category=='#???#':
			out.append('PTEXT')
		else:
			out.append(category[0])
		out.append(str(len(block)))
		out.append(a)
		out.append(b)
		out.append(c)
		out.append(d)
		out.append(e)
		out.append(f)
		out.append(g)
		out.append(h)
		out.append(i)
		out.append(j)
		out.append(k)
		out.append(l)
		out.append(m)
		out=','.join(out)
		print >> fo, out


def nnHeadLikelihood(block):
	keywords=['from:','subject:','sender:','date:','keywords:','article:','organization:']
	emailCnt=0
	for line in block:
		words=line.split()
		if len(words)>1:
			if words[1].lower() in keywords:
				emailCnt+=1 
	return str(emailCnt)

def quotedLikelihood(block):
	quoteCnt=0
	for line in block:
		if re.match(r'^.*\s[>:]',line) or re.match(r'^.*\sCJK>',line) or re.match(r'^.*wrote:$',line) or re.match(r'^.*writes:$',line):
			quoteCnt+=1
	if len(block)==0:
		return 0
	else:
		return str(float(quoteCnt)/float(len(block)))

def signatureImportant(block):
	firstLine=line.split()
	if len(firstLine)>=2:		
		if firstLine[1]=='--':
			return '1'
		else:
			return '0'
	else:
		return '0'

def signatureLikelihood(block):
	hasName=0
	sigCnt=0
	for line in block:
		if re.match(r'^.*\|',line) or re.match(r'^.*====',line) or re.match(r'^.*\[\]\[\]',line) or re.match(r'^.*\/\\',line) or re.match(r'^.*\*\*',line):
			sigCnt+=1
		if re.match(r'^.*[A-Z]',line):
			hasName=1
 	return str(float(sigCnt)/float(len(block))*hasName)

def graphicLikelihood(block):
	numOfGraphic=0
	for line in block:
		if len(re.findall(r'_|\/|\\|\*|\(|\)|\~|\^|\-|\||\so\s',line))!=0:
			numOfGraphic+=len(re.findall(r'_|\/|\\|\*|\(|\)|\~|\^|\-|\||\so\s',line)) 
	return str(float(numOfGraphic)/float(len(block)))

def tableLikelihood(block):
	avg=0
	wordssum=0
	for line in block:
		words=line.split()
		wordssum+=len(words)
	avg=float(wordssum)/float(len(block))
	variance=0
	for line in block:
		words=line.split()
		variance+=float((avg-len(words))**2)*(1/float(len(block)))
	return str(variance)

def addresslikelihood(block):
	likelihood=0
	for line in block:
		words=line.split()
		for word in words:
			if re.match(r'tel:|fax:|email:|phone:',word.lower()):
				likelihood+=1
			if word.lower() in stateAbbrevs:
				likelihood+=1
	return str(float(likelihood)/float(len(block)))

def itemlikelihood(block):
	likelihood=0
	for line in block:
		words=line.split()
		if len(words)<2:
			continue
		firstWord=words[1]
		if re.match(r'^[1-9]',firstWord):
			likelihood+=1
		if re.match(r'\)$',firstWord):
			likelihood+=1
		if re.match(r'^\(',firstWord):
			likelihood+=1
		if re.match(r'.$',firstWord):
			likelihood+=1

	return str(likelihood)

def headerEndinPeriod(block):
	period=0
	for line in block:
		if re.match(r'\.$',line):
			period=1
			break
	return str(period)

def headerCapitalized(block):
	cnt=0
	wdcnt=0
	for line in block:
		words=line.split()
		for word in words:
			wdcnt+=1
			if re.match(r'^[A-Z]',word):
				cnt+=1
				if re.match(r'^[A-Z]+$',word):
					cnt+=1
	return str(float(cnt)/float(wdcnt))

def headerIndented(block):
	cnt=0
	words=block[0].split()
	cat=words[0]
	for line in block:
		l=line[len(cat):len(line)]
		cnt+=(len(l.rstrip())-len(l.strip()))
	return str(float(cnt)/float(len(block)))

def wordsPerLine(block):
	cnt=0
	for line in block:
		words=line.split()
		cnt+=len(words)
	return str(float(cnt)/float(len(block)))

def blanksPerLine(block):
	cnt=0
	for line in block:
		words=line.split()
		cnt+=(len(line)-len(''.join(words)))
	return str(float(cnt)/float(len(block)))



block=[]
for line in data:
	line=line.strip('\n')
	category=line.split()
	
	if category[0]=='#BLANK#':
		if len(block)==0:
			block=[]
			continue
		ProcessPreviousBlock(block)
		block=[]
	else:
		block.append(line)
