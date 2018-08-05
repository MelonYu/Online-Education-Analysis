#!/usr/bin/env python

# -*- encoding: utf-8 -*-

"""
@Author  :   Amelia 
@Contact :   yu_mengling@hust.edu.cn
@File    :   html_downloader.py
 
@Time    :   18-6-30 下午7:04
"""

# 根据url下载相应的页面

import requests


class HtmlDownloader(object):
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
                        'Host': 'www.imooc.com',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-GB,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Referer': 'https://www.imooc.com/course/list',
                        }

    def download(self, url):
        if url is None:
            return None
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return None
        return response.text  # html_cont
