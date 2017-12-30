# coding=utf-8
import urllib
import re
from urlparse import urljoin
from bs4 import BeautifulSoup

LOCALDEBUG = True



infobox_ref = "xlore20170407/wikiExtractResult/frwiki-infobox.dat"
a_fr_en_ref = "xlore20170407/wikiExtractResult/frwiki-fr-en-langlink.dat"
prop_fr_en_ref = "xlore20170407/wikiExtractResult/frwiki-fr-en-property.dat"
a_fr_en={}
prop_fr=[]

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

if(not LOCALDEBUG):
	readmap()
	infobox=open(infobox_ref,"r")
	open(prop_fr_en_ref,"w").close()
	out = prop_fr_en_ref
else:
	infobox=["Cygnus X-1\t\t"]
	out="test"



for article in infobox:
	if not re.search("\t\t",article):
		continue
	linkname=re.search("^(.+?)\t\t",article).group(1)
	print linkname
	urlBase = "http://fr.wikipedia.org/"
	url = urlBase + "wiki/%s" % linkname
	try:
		soup = BeautifulSoup(urllib.urlopen(url), 'html.parser')
	except Exception:
		import traceback
		print "CONNECTION ERROR: " + traceback.format_exc()
		continue
	isInfobox = lambda x: x and x.startswith("infobox")
	isThValid = lambda x: x.name!="div";
	#n=0
	#soup_en = soup.find(class_="mw-body").find(id="bodyContent").find(class_="infobox").find_all("tr",class_=isTrValid, limit=200)
	if not soup.find(class_=isInfobox):
		continue
	for i in soup.find(class_=isInfobox).find_all("tr", limit=200):
		#if n==0: n+=1; continue;
		#n+=1
		th = i.find("th",colspan=False)
		if th: #text=true
			if th.div:
				th.div.decompose()
			if th.span:
				th.span.decompose()
			if th.small:
				th.small.decompose()
			text = th.text.encode('utf-8').strip()
			if "\n" in text:
				text = text[:text.find("\n")+1].strip()
			if text and not text in prop_fr:
				if text in a_fr_en:
					writeToFile(out,text,a_fr_en[text])

				elif th.a and th.has_attr("title"):
					a=th.a["title"].encode('utf-8')
					if a in a_fr_en and not text in prop_fr:
						writeToFile(out,text,a_fr_en[a],True)
					else:
						print text, "NO!"
				else:
					print text, "NO"
					#TODO : DISAMBIGUATION

