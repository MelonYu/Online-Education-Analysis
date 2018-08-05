#!/usr/bin/env python

# -*- encoding: utf-8 -*-

"""
@Author  :   Amelia 
@Contact :   yu_mengling@hust.edu.cn
@File    :   test_userdetail.py
 
@Time    :   18-7-17 下午9:50
"""

''' 慕课网用户页'''
# import threading

import time
from typing import Dict, Any, Union

import requests
from bs4 import BeautifulSoup
import pymysql


# 慕课网 python
# https://www.imooc.com/u/1857206/courses 第一个用户？ 到6946586
# url中有两个变量： user_id, page_num

FIRST_USER = 1857210  # 1857206
LAST_USER = 6946586  # 6900000
user_id = 1857206  # the first user  #2481691

base_url = 'https://www.imooc.com/u/'
page_url = '/courses?page='  # + page_num  # 可能有多个page
# url = 'https://ke.qq.com/course/list/python'

headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}

# urls = []
# def generate_urls(FIRST_USER, LAST_USER):
#     rLock = threading.RLock()


for user_id in range(FIRST_USER, LAST_USER):
    user_url = base_url + str(user_id) + '/courses'
    res = requests.get(user_url, headers=headers)
    if res.status_code != 200:
        print('user %s not exist' % user_id)
        break

    html_doc = res.text
    # print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')
    # course_list = soup.find_all("div",class_="course-list-cont")
    # #    print course_list
    # for course in course_list:
    #     print course

    user_detail = soup.find('div', class_='user-info clearfix')
    user_info = {}
    user_info['sex'] = '无'
    user_info['province'] = '无'
    user_info['city'] = '无'
    user_info['city'] = '无'
    user_info['career'] = '无'

    user_info['user_id'] = user_id
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
        page_num = 1

    # for k in user_info.keys():
    #     print('%s:%s' % (k, user_info[k]))

    # --------------------------------------------------------------------------------------------------
    # 将用户基本数据写入数据库

    sql_user = 'INSERT INTO user_basic_info (' \
               'user_id,user_name, sex, user_pic_url, user_sign, province, city, career, total_study_duration,'\
               'exp, coins, follows, fans) ' \
               'VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %d, %d, %d, %d);' % \
               (int(user_info['user_id']), user_info['user_name'], user_info['sex'], user_info['user_pic_url'],
                user_info['user_sign'], user_info['province'],user_info['city'], user_info['career'],
                user_info['total_study_duration'],
                int(user_info['exp']), int(user_info['coins']), int(user_info['follows']), int(user_info['fans']))
    print(sql_user)

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "IMOOC_COURSE", use_unicode=True, charset="utf8")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 语句
    # 一页内的数据，按条插入数据库

    # cursor.execute(sql)
    try:
        # 执行sql语句
        cursor.execute(sql_user)
        # 提交到数据库执行
        db.commit()
        print("[ok] user info: commit to database")
    except:
        # 如果发生错误则回滚
        db.rollback()

    # 关闭数据库连接
    db.close()

    # time.sleep(2)

    # -------------------------------------------------------------------------------------------------
    # ???
    # https: // www.imooc.com / u / 1857211 / courses?page = 1
    # Traceback(most recent call last): File
    # "/home/amelia/program-basic/Online-Education-Analysis/imooc_spider/test_userdetail.py", line 150, in < module >
    # study_time = course.find('span').get_text().strip()
    # AttributeError: 'NoneType' object has no attribute 'find'
    for page_id in range(1, page_num+1):
        url = base_url + str(user_id) + page_url + str(page_id)
        print(url)
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print('user %s not exist' % user_id)
            continue
        html_doc = res.text
        # print(html_doc)
        soup = BeautifulSoup(html_doc, 'html.parser')
        first_course = soup.find("div", class_="clearfix tl-item tl-item-first")
        course_list = soup.find_all("div", class_="clearfix tl-item ")

        course_list.insert(0, first_course)

        page_pro = []

        if course_list is None:
            continue
        for course in course_list:
            #   print(course)
            study_time = course.find('span').get_text().strip()
            year, date = study_time.split('\n')

            cour = course.find_all('div', class_="course-list-cont")
            for cha in cour:
                pro = {}
                pro['user_id'] = user_id
                pro['recent_study_date'] = year + u'年' + date
                h3 = cha.find('h3', class_='study-hd').find('a')
                pro['course_name'] = h3.get_text()
                pro['course_url'] = h3['href']

                # h3 = cha.find('h3', class_='study-hd').find('a')
                # pro['course_name'] = h3.get_text()
                # pro['course_id'] = h3['href']

                study_points = cha.find('div', class_='study-points').contents
                pro['has_learn'] = study_points[1].get_text()[2:]
                pro['time_consuming'] = study_points[3].get_text()
                pro['study_to'] = study_points[5].get_text()

                catog_points = cha.find('div', class_='catog-points').contents
                pro['note_num'] = catog_points[1].get_text()[3:]
                pro['code_num'] = catog_points[3].get_text()[3:]
                pro['ques_num'] = catog_points[5].get_text()[3:]

                # for k in pro.keys():
                #     print('%s:%s' % (k, pro[k]))
                # print('\n')
                page_pro.append(pro)

        # print(page_pro)
        # 打开数据库连接
        db = pymysql.connect("localhost", "root", "123456", "IMOOC_COURSE", use_unicode=True, charset="utf8")
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 语句
        # 一页内的数据，按条插入数据库

        for p in page_pro:
            sql = 'INSERT INTO user_learn_detail (' \
                  'user_id, course_url, course_name, recent_study_date, has_learn, time_consuming, study_to,' \
                  'note_num, code_num, ques_num) ' \
                  'VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\',' \
                  ' %d, %d, %d);' % \
                  (int(p['user_id']), p['course_url'], p['course_name'], p['recent_study_date'],
                   p['has_learn'], p['time_consuming'], p['study_to'],
                   int(p['note_num']), int(p['code_num']), int(p['ques_num']))
            print(sql)

            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print("ok! commit to database")

            except:
                # 如果发生错误则回滚
                db.rollback()

        # 关闭数据库连接
        db.close()

        time.sleep(3)


# if __name__ == '__main__':
#     pass
