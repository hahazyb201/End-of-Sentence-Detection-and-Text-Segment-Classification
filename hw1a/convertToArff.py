import re
import sys
program_name = sys.argv[0]
file_name=sys.argv[1]

f=open("data.arff","w")




print >> f, "@RELATION EOS_NEOS";

print >> f, "@ATTRIBUTE class   {EOS,NEOS}";
print >> f, "@ATTRIBUTE R1islower   {1,0}";

print >> f, "@ATTRIBUTE L1isTitle   {1,0}";

print >> f, "@ATTRIBUTE L1isAbbrevs   {1,0}";

print >> f, "@ATTRIBUTE L1isInternal   {1,0}";

print >> f, "@ATTRIBUTE L1isTimeterm   {1,0}";

print >> f, "@ATTRIBUTE L1isUnlikely   {1,0}";

print >> f, "@ATTRIBUTE Comma   {1,0}";

print >> f, "@ATTRIBUTE Period   {1,0}";

print >> f, "@ATTRIBUTE L1isUpper   {1,0}";

print >> f, "@ATTRIBUTE R1isUpper   {1,0}";
print >> f, "@ATTRIBUTE L1isNum   {1,0}";

print >> f, "@ATTRIBUTE L1R1isQuestionMarkExclamation   {1,0}";
print >> f, "@ATTRIBUTE L1P   {1,0}";
print >> f, "@ATTRIBUTE R1P   {1,0}";
print >> f, "@ATTRIBUTE R1isCommaPeriod   {1,0}";
print >> f, "@ATTRIBUTE L1Length   NUMERIC";
print >> f, "@ATTRIBUTE R1Length   NUMERIC";
print >> f, "@ATTRIBUTE Llength   NUMERIC";
print >> f, "@ATTRIBUTE Rlength   NUMERIC";
print >>f, "@ATTRIBUTE Nspace   NUMERIC";

print >> f, "@DATA";

def generateSet(file):
	fileSet=set()
	line=file.readline()
	line=line.strip('\n')
	while line:
		fileSet.add(line)
		line=file.readline()
		line=line.strip('\n')
	return fileSet

title=open("classes/titles",'r')
abbrevs=open("classes/abbrevs",'r')
internal=open("classes/sentence_internal",'r')
timeterms=open("classes/timeterms",'r')
unlikely=open("classes/unlikely_proper_nouns",'r')
	
titleSet=generateSet(title)
abbrevsSet=generateSet(abbrevs)
internalSet=generateSet(internal)
timetermsSet=generateSet(timeterms)
unlikelySet=generateSet(unlikely)

data=open(file_name,'r')
for line in data:
	args=line.split()
	cla=args[0]
	idnum=args[1]
	L3=args[2]
	L2=args[3]
	L1=args[4]
	p=args[5]
	R1=args[6]
	R2=args[7]
	R3=args[8]
	Llength=args[9]
	Rlength=args[10]
	NumSpace=args[11]
	
	out=[]
	out.append(cla)
	if re.match(r'^[a-z]',R1):
		out.append('0')
	else:
		out.append('1')
	
	if L1.lower() in titleSet:
		out.append('0')
	else:
		out.append('1')
	
	if L1.lower() in abbrevsSet:
		out.append('0')
	else:
		out.append('1')
	
	
	if L1.lower() in internalSet:
		out.append('0')
	else:
		out.append('1')

	if L1.lower() in timetermsSet:
		out.append('0')
	else:
		out.append('1')

	if L1.lower() in unlikelySet:
		out.append('0')
	else:
		out.append('1')
	
	if re.match(r'\,',L1) or re.match(r'\,',L2) or re.match(r'\,',R1) or re.match(r'\,',R2) or re.match(r'\,',R3) or re.match(r'\,',L3):
	    out.append('0')
	else:
		out.append('1')

	if re.match(r'\.',L1) or re.match(r'\.',L2) or re.match(r'\.',R1) or re.match(r'\.',R2) or re.match(r'\.',R3) or re.match(r'\.',L3):
		out.append('0')
	else:
		out.append('1')

	if re.match(r'^[A-Z][a-z]*$',L1):
		out.append('0')
	else:
		out.append('1')
	
	if re.match(r'^[A-Z][a-z]*',R1):
		out.append('1')
	else:
		out.append('0')

	if re.match(r'[0-9]+',L1):
		out.append('0')
	else:
	    out.append('1')
	
	if re.match(r'\?|\!',L1) or re.match(r'\?|\!',R1):
		out.append('0')
	else:
		out.append('1')

	if L1=='<P>':
		out.append('0')
	else:
		out.append('1')

	if R1=='<P>':
		out.append('0')
	else:
		out.append('1')
	if re.match(r'\,|\.',R1):
		out.append('0')
	else:
		out.append('1')
	out.append(str(len(L1)))
	out.append(str(len(R1)))
	out.append(Llength)
	out.append(Rlength)
	out.append(NumSpace)
	
	out=','.join(out)
	print >> f, out
