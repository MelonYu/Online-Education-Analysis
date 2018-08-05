#!/usr/bin/env python

# -*- encoding: utf-8 -*-

"""
@Author  :   Amelia 
@Contact :   yu_mengling@hust.edu.cn
@File    :   spider_main.py
 
@Time    :   18-6-30 下午6:55
"""

# 爬取慕课网免费课程列表页
# 根据获得的免费课程的url,爬取该课程相关的详细信息

import url_manager
import html_downloader
import html_parser
import save_result


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = save_result.DataBaseOutputer()

    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        # 待爬取的url
        while self.urls.has_new_url():
            try:
                # 获取一个待爬取的url
                new_url = self.urls.get_new_url()
                # print('craw %d : %s' % (count, new_url))
                # 启动下载器
                html_cont = self.downloader.download(new_url)
                # 解析器，解析页面数据包
                freecourse_card = self.parser.parse_freecourse_card(new_url, html_cont)
                new_urls, new_data = self.parser.paser(new_url, html_cont)  # 得到新的列表，以及新的数据
                # 添加进rul管理器
                self.urls.add_new_urls(new_urls)
                # 搜集数据
                self.outputer.collect_data(new_data)
                # if count == 20:
                #     break
                # count = count + 1
            except:
                print("爬取失败")
            # 输出搜集好的数据
        self.outputer.output_mysql()
        # ss = self.urls.getUtls()
        # print(ss)


if __name__ == "__main__":
    root_utl = "https://www.imooc.com/course/list"     # ?sort=pop&page="
    obj_spider = SpiderMain()
    obj_spider.craw(root_utl)

