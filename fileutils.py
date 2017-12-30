def readmap():
        # Read list of all en/zh articles
        for line in open(a_fr_en_ref,"r"):
            stemp = line.strip().split("\t\t")
            if len(stemp)!=2:
                print stemp
            else:
                a_fr_en[stemp[0]]=stemp[1]
        print 'reading data finish...','article refmap size:',len(a_fr_en)

def writeToFile(fname,left,right,chevron=False):
	prop_fr.append(left)
	with open(fname,"a") as out:
		out.write(left + "\t" + right + "\n")
	if chevron:
		print (left + "\t>> " + right)
	else:
		print (left + "\t" + right)

def printu(ustr):
    print(ustr.encode('utf-8'))