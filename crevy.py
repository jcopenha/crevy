#!/usr/bin/env python
import XRecord
db = XRecord.connect('mysql', name='jcopenha', host='localhost', 
                     port=3306, user='root', password='password')
for post in db.XArray("wp_posts"):
    if post.post_type == "post":
        print post.post_title, post.post_type, post.post_modified
