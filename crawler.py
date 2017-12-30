import urllib
import lxml.etree as etree
import mwparserfromhell
from fileutils import readmap, writeToFile



title = "Georges St-Pierre"

params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"content" }
params["titles"] = "API|%s" % urllib.quote(title.encode("utf8"))
qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
url = "http://fr.wikipedia.org/w/api.php?%s" % qs
tree = etree.parse(urllib.urlopen(url))
revs = tree.xpath('//rev')

print "The Wikipedia text for", title, "is"
text = revs[-1].text

text = text.replace('\n','').replace('\t','').encode('utf-8')
wikicode = mwparserfromhell.parse(text)
tpls = wikicode.filter_templates(recursive=False)
i=0
for node in tpls:
	if node.name.startswith('Infobox'):
		Infobox_idx=i
	i+=1


for nod in tpls[Infobox_idx].params:
	print nod.name.encode('utf-8')

