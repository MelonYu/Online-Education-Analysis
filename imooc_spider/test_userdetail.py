#!/usr/bin/env python

# -*- encoding: utf-8 -*-

"""
@Author  :   Amelia 
@Contact :   yu_mengling@hust.edu.cn
@File    :   test_userdetail.py
 
@Time    :   18-7-17 下午9:50
"""

''' 慕课网用户页'''
import time
from typing import Dict, Any, Union

import requests
from bs4 import BeautifulSoup
import pymysql

# 慕课网 python
# https://www.imooc.com/u/1857206/courses 第一个用户？ 到6900000
# url中有两个变量： user_id, page_num
FIRST_USER = 2481691  # 1857206
LAST_USER = 2481692  # 6900000
user_id = 1857206  # the first user  #2481691

base_url = 'https://www.imooc.com/u/'
page_url = '/courses?page='  # + page_num  # 可能有多个page
# url = 'https://ke.qq.com/course/list/python'

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}

for user_id in range(FIRST_USER, LAST_USER):
    user_url = base_url + str(user_id) + '/courses'
    res = requests.get(user_url, headers=headers)
    if res.status_code != 200:
        print('user %s not exist' % user_id)
        break

    html_doc = res.text
    # print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
    # course_list = soup.find_all("div",class_="course-list-cont")
    # #    print course_list
    # for course in course_list:
    #     print course

    user_detail = soup.find('div', class_='user-info clearfix')
    user_info = {}
    user_info['user_pic_url'] = user_detail.find('img')['src']
    user_info['user_name'] = user_detail.find('h3', class_='user-name clearfix').span.get_text()

    about = user_detail.find('p', class_='about-info').contents
    about_name_list = ['sex', 'province', 'city', 'career']
    for i, sp in enumerate([x for x in about[:-2] if x != '\n']):
        user_info[about_name_list[i]] = sp.get_text().strip()

    user_info['user_sign'] = user_detail.find('p', class_='user-desc').get_text()

    study_info = user_detail.find_all('div', class_='item follows')
    study_info_name_list = ['total_study_duration', 'exp', 'coins', 'follows', 'fans']
    for i, st in enumerate(study_info):
        st_text = st.get_text().strip().split('\n')
        user_info[study_info_name_list[i]] = st_text[0]
    try:
        page_info = soup.find('div', class_='page').contents
        page_num = int(page_info[-1]['href'].split('=')[-1])
    except:
        page_num = 2

    for k in user_info.keys():
        print('%s:%s' % (k, user_info[k]))

    for page_id in range(1, page_num):
        url = base_url + str(user_id) + page_url + str(page_id)
        print(url)
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print('user %s not exist' % user_id)
            continue
        html_doc = res.text
        # print(html_doc)
        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
        course_list = soup.find_all("div", class_="clearfix tl-item ")
        for course in course_list:
            study_time = course.find('span').get_text().strip()
            year, date = study_time.split('\n')

            cour = course.find_all('div', class_="course-list-cont")
            for cha in cour:
                pro = {}
                pro['recent_study_date'] = year + u'年' + date
                h3 = cha.find('h3', class_='study-hd').find('a')
                pro['course_name'] = h3.get_text()
                pro['course_id'] = h3['href']
                for k in pro.keys():
                    print('%s:%s' % (k, pro[k]))
                print('\n')

# if __name__ == '__main__':
#     pass
