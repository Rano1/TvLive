# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

__author__ = 'hstking hstking@hotmail.com'


class CustomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
        request.headers.setdefault('User-Agent', ua)
