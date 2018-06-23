#!/usr/bin/env python

# -*- encoding: utf-8 -*-

"""
@Author  :   Amelia 
@Contact :   yu_mengling@hust.edu.cn
@File    :   freecourse.py
 
@Time    :   18-6-2 下午3:58
"""

import time
from typing import Dict, Any, Union

import requests
from bs4 import BeautifulSoup
import pymysql

# 慕课网

# url管理
imooc_url = 'https://www.imooc.com'

base_url = 'https://www.imooc.com/course/list?sort=pop&page='
page_url = [base_url + str(i) for i in range(1, 36)]
print(page_url)

# url下载
headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
           # 'Host': 'www.imooc.com',
           # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           # 'Accept-Language': 'en-GB,en;q=0.5',
           # 'Accept-Encoding': 'gzip, deflate, br',
           # 'Referer': 'https://www.imooc.com/course/list'
           }

for url in page_url:
    print(url)
    courses_info = []

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print('%s craw wrong' % url)
        continue

    html_doc = res.text
    # 解析html
    soup = BeautifulSoup(html_doc, 'html.parser')
    course_list = soup.find_all("div", class_="course-card-container")

    for course in course_list:
        # print(course)
        info = {}
        # course_url, image_url, course_label, course_name, course_grade, course_population, course_desc
        info['course_url'] = imooc_url + course.a['href']
        info['image_url'] = 'https:' + course.img['src']
        info['course_label'] = ' '.join([i.get_text() for i in course.find_all("label")])
        info['course_name'] = course.h3.get_text()
        info['course_grade'] = course.find("span").get_text()
        info['course_population'] = course.find("span").next_sibling.get_text()
        info['course_desc'] = course.p.get_text()

        courses_info.append(info)
    # print(courses_info)

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "IMOOC_COURSE", use_unicode=True, charset="utf8")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 语句
    # 一页内的数据，按条插入数据库
    for c in courses_info:
        # print(c['course_url'])
        sql = 'INSERT INTO free_course_info (' \
              'course_url, image_url, course_label, course_name, course_grade, course_population, course_desc) ' \
              'VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %d, \'%s\');' % \
              (c['course_url'], c['image_url'], c['course_label'], c['course_name'], c['course_grade'],
               int(c['course_population']), c['course_desc'])
        # print(sql)
        # sql = sql.encode("utf-8").decode("latin1")
        # cursor.execute(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

    # 关闭数据库连接
    db.close()

    time.sleep(10)

# if __name__ == '__main__':
#     pass
