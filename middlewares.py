# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import base64



# for Python3
# proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


proxyServer = "http://http-dyn.abuyun.com:9020"
proxyUser = "H812EYV2X1LH984D"
proxyPass = "DE713508038C4A8A"
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

class ABProxyMiddleware(object):
    """ 阿布云ip代理配置 """
    def process_request(self, request, spider):
        request.headers["Proxy-Authorization"] = proxyAuth
        request.meta["proxy"] = proxyServer
