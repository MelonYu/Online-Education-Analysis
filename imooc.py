# -*- coding=utf8 -*-

import urllib2
from bs4 import BeautifulSoup
import requests

# urllib2 下载url的网页内容

# 慕课网 python
url = 'https://www.imooc.com/course/list?page=1'

request = urllib2.Request(url)
request.add_header("user-agent","Mozilla/5.0")
res = urllib2.urlopen(request)
filename = 'imooc_page_1.txt'

if res.getcode() == 200:
    
    html_doc = res.read()
    with open(filename,'w') as f:
    	f.write(html_doc)
    	
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
    course_list = soup.find_all("div",class_="course-card-container")
#    print course_list
    # for course in course_list[0]:
    #     print(course)
        
else:
    print('code: %d'%res.getcode())