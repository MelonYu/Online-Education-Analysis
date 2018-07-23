#!/usr/bin/env python

# -*- encoding: utf-8 -*-

"""
@Author  :   Amelia 
@Contact :   yu_mengling@hust.edu.cn
@File    :   test_courseinfodetail.py
 
@Time    :   18-7-18 下午11:08
"""

''' 慕课网免费课程详情页'''
import time
from typing import Dict, Any, Union

import requests
from bs4 import BeautifulSoup
import pymysql

# 慕课网 python
# https://www.imooc.com/learn/85  其中id可以直接从免费课程卡片页获取
# url中有两个变量： user_id, page_num

base_url = 'https://www.imooc.com/learn/'

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}

for course_id in range(80, 86):
    user_url = base_url + str(course_id)
    res = requests.get(user_url, headers=headers)
    if res.status_code != 200:
        print('course %s not exist' % course_id)
        break

    html_doc = res.text
    # print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
    # course_list = soup.find_all("div",class_="course-list-cont")
    # #    print course_list
    # for course in course_list:
    #     print course

    path_detail = soup.find('div', class_='path')
    print(path_detail.get_text())


# if __name__ == '__main__':
#     pass