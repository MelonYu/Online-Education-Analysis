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

for course_id in range(85, 86):
    user_url = base_url + str(course_id)
    res = requests.get(user_url, headers=headers)
    if res.status_code != 200:
        print('course %s not exist' % course_id)
        continue

    html_doc = res.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    # course_list = soup.find_all("div",class_="course-list-cont")
    # #    print course_list
    # for course in course_list:
    #     print course
    course_detail = {}
    path_detail = soup.find('div', class_='path').get_text().strip()
    course_tip = soup.find_all("dd")
    course_tip_first = course_tip[0].get_text()
    course_tip_second = course_tip[1].get_text().strip()
    teacher_info = soup.find('span', class_="tit").find("a")
    teacher_name = teacher_info.get_text().strip()
    teacher_url = teacher_info["href"]
    teacher_job = soup.find("span", class_="job").get_text()
    course_info = soup.find_all("span", class_="meta-value")
    course_duration = course_info[1].get_text()
    course_score = course_info[3].get_text()
    menu_pp = soup.find("ul", class_="course-menu").find_all("span")
    comment_pp = menu_pp[0].get_text()
    score_pp = menu_pp[1].get_text()

    # course_detail['']


    print(path_detail)
    print(course_tip_first)
    print(course_tip_second)
    print(teacher_name)
    print(teacher_url)
    print(teacher_job)
    # print(course_info)
    print(comment_pp)
    print(score_pp)
    print("done")


# if __name__ == '__main__':
#     pass