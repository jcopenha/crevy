#!/usr/bin/env python
import datetime
import XRecord

class Page:
    def __init__(self, title, link, date, content):
        self.title = title
        self.link = link
        self.date = date
        self.content = content
        # should start with <p>
        # 0x13 0x10 - two in a row is </p><p>
        # 0x13 0x10 - only one it <br />
        self.content = "<p>" + self.content
        self.content = self.content.replace("\r\n\r\n","</p><p>")
        self.content = self.content.replace("\r\n","<br />")
        self.content = self.content + "</p>"
        # need two links 
        # typedef.org/jcopenha/title
        # typedef.org/jcopenha/year/month/day/title
        # TOC can just link to first one but we'll have to generate two html files

    def tohtml(self):
        file = open(self.link+".html","wt")
        file.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\n")
        file.write("\"http://www.w3.org/TR/html4/strict.dtd\">\n")
        file.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"simple.css\">\n")
        file.write("<body>\n")
        file.write("<div id=\"wrap\">\n")
        file.write("<div id=\"header\">\n")
        file.write(self.title)
        file.write("</div>\n")
        file.write("<div id=\"main\">\n")
        file.write(self.content)
        file.write("</div>\n")
        file.write("<div id=\"footer\">\n")
        file.write("<a href=\"index.html\">HOME</a>\n")
        file.write("</div>\n")
        file.write("</div>\n")
        file.write("</body>\n")
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
        file.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01//EN\n")
        file.write("\"http://www.w3.org/TR/html4/strict.dtd\">\n")
        file.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"simple.css\">\n")
        print >>file, "<HTML><BODY>"
        file.write("<div id=\"wrap\">\n")
        file.write("<div id=\"main\">\n")
        print >>file, "<p>After running my blog with Drupal and then WordPress"
        print >>file, " I've finally switched to completely static pages. I stopped"
        print >>file, " updating a long time ago so no big loss.</p>"
        print >>file, "<p>You can find me on twitter as <a href=\"http://www.twitter.com/jcopenha\">@jcopenha</a>"
        print >>file, "and on most other social sites as jcopenha</p>"
        print >>file, "<UL>"
        
        for p in self.pages:
            print >>file, "<LI>", self.makelink(p.title, p.link)

        print >>file, "</UL>"
        file.write("</div>\n")
        file.write("</div>\n")
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
