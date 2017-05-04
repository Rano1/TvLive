# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware

__author__ = 'hstking hstking@hotmail.com'

# 自定义UserAgent
class CustomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
        request.headers.setdefault('User-Agent', ua)

# 自定义中间键代理，可以通过代理列表获取
class CustomProxy(HttpProxyMiddleware):
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://203.70.11.186:80'