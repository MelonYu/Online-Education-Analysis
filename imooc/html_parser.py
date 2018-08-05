#!/usr/bin/env python

# -*- encoding: utf-8 -*-

"""
@Author  :   Amelia 
@Contact :   yu_mengling@hust.edu.cn
@File    :   html_parser.py
 
@Time    :   18-6-30 下午7:05
"""

# 解析页面，得到想抓取的结果，并将结果返回

import requests
from bs4 import BeautifulSoup


class HtmlParser(object):
    def __init__(self):
        self.base_url = "https://www.imooc.com"

    #获取新的地址，返回一个集合
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"/item/\S+"))
        for link in links:
            #匹配a标签里面的href属性
            new_url = link['href']
            #把循环出来的地址进行拼接
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            #放入集合
            new_urls.add(new_full_url)
        return new_urls

    #把反回来的值对应的存入字典里面
    def _get_new_data(self, page_url, soup):
        res_data = {}
        res_data['url'] = page_url
        # <dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>

        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')
        res_data['title'] = title_node.get_text()

        # <div class="lemma-summary" label-module="lemmaSummary">
        summary_node = soup.find('div', class_='lemma-summary')
        res_data['summary'] = summary_node.get_text()
        return res_data

    def paser(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        #print(soup)
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def parse_freecourse_card(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        courses_info = []
        course_list = soup.find_all("div", class_="course-card-container")
        for course in course_list:
            # print(course)
            info = { }
            # course_url, image_url, course_label, course_name, course_grade, course_population, course_desc
            info['course_url'] = self.base_url + course.a['href']
            info['image_url'] = 'https:' + course.img['src']
            info['course_label'] = ' '.join([i.get_text() for i in course.find_all("label")])
            info['course_name'] = course.h3.get_text()
            info['course_grade'] = course.find("span").get_text()
            info['course_pp'] = course.find("span").next_sibling.get_text()
            info['course_desc'] = course.p.get_text()

            courses_info.append(info)

        return courses_info
