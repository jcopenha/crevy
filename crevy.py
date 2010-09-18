#!/usr/bin/env python
import datetime
import XRecord

class Page:
    def __init__(self, title, link, date, content):
        self.title = title
        self.link = link
        self.date = date
        self.content = content
        # need two links 
        # typedef.org/jcopenha/title
        # typedef.org/jcopenha/year/month/day/title
        # TOC can just link to first one but we'll have to generate two html files

    def tohtml(self):
        file = open(self.link+".html","wt")
        file.write(self.content)
        file.close()

class TOC:
    def __init__(self):
        self.pages = list()

    def addPage(self, title, link, date, content):
        format = "%Y-%m-%d %H:%M:%S"
        self.pages.append(Page(title, 
                               link, 
                               datetime.datetime.strptime(str(date), format),
                               content))

    def makelink(self, title, link):
        html = "<A HREF=\""+str(link)+".html\">"+str(title)+"</A>"
        return html

    def outputTOC(self):
        self.pages.sort(lambda x, y: cmp(x.date, y.date))
        self.pages.reverse()

        file = open("index.html", "wt")
        print >>file, "<HTML><BODY>"
        print >>file, "<UL>"
        
        for p in self.pages:
            print >>file, "<LI>", self.makelink(p.title, p.link)

        print >>file, "</UL>"
        print >>file, "</BODY></HTML>"
        file.close()

        for p in self.pages:
            p.tohtml()


toc = TOC()
db = XRecord.connect('mysql', name='jcopenha', host='localhost', 
                     port=3306, user='root', password='password')
for post in db.XArray("wp_posts"):
    if post.post_type == "post":
        # no idea why i have non-ascii values in the DB but I do
        # and 'write' complains about them, so we'll filter them out
        content = ''.join([x for x in post.post_content if ord(x) < 128])
        toc.addPage(post.post_title, post.post_name, post.post_date, content)

toc.outputTOC()
