#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import re
import urllib2

class importPaper :
  def __init__(self, paper_infors) :
    decoded_message = str(paper_infors).decode('utf8')
    self.all_info = decoded_message
    self.infos = {}
    self.status = "Not yet published"
    for line in decoded_message.split(',') :
      li = line.strip()
      words = li.split('=',1)
      if ( len ( words) != 2 ) : continue
      self.infos[words[0].strip()] = re.sub(' +',' ',words[1].strip().replace('\n',"").replace('\"',""))
    if "journal" in self.infos :
      if ( self.infos["journal"].find("Submitted" ) != -1 or not "pages" in self.infos ) :
        self.status = "Submitted"
      else : 
        self.status = "Published"
    if "number" in self.infos :
      self.infos["volume"] +="(%s)"%(self.infos["number"])
    self.infos["title"] = self.infos["title"][1:-1]
  def dumpInfo(self) :
    print self.infos
  def printOriginal(self) :
    print self.all_info
  def printInfo(self) :
    print (self.infos["title"]+","+"CMS Collaborator"+","+","+self.infos["journal"]+","+self.infos["volume"]+","+self.infos["pages"]+","+"SCI"+","+"ISBN"+","+"DATE"+","+"dx.doi.org/"+self.infos["doi"]).encode("utf-8")
  def isPublished(self) :
    #print self.status
    return self.status == "Published" 
      
url ="http://inspirehep.net/search?ln=en&ln=en&p=find+a+Ryu%2C+Geonmo+and+date+2016.1.1.-%3E2016.12.31&of=hx&action_search=Search&sf=&so=d&rm=&rg=250&sc=0"
handle = urllib2.urlopen(url)
data = handle.read()
soup = BeautifulSoup(data)
#article = str( soup('div', {'class':'article',}) )
#print article.decode('utf8')

published_papers=[]
for x in  soup('pre') :
  paper = importPaper(x)
  if ( paper.isPublished() ) : 
    paper.printInfo()


