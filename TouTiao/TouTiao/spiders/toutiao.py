# -*- coding: utf-8 -*-
import scrapy
import json
from TouTiao.items import ToutiaoItem
from urllib.parse import urlencode
import re
import urllib.request
from lxml import etree

def get_page_index(start_url,offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
    }
    url = start_url + urlencode(data)
    return url

class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.com']
    keyword = "丽水山耕"
    offset = 0
    start_url = 'https://www.toutiao.com/search_content/?'
    url = get_page_index(start_url, offset, keyword)
    start_urls = [url]

    def parse(self, response):
        dic = json.loads(response.text)
        if dic and 'data' in dic.keys():
            for node in dic.get('data'):
                item = ToutiaoItem()
                try:
                    item['theme'] = node.get("title")
                    item['comments_count'] = node.get("comments_count")
                    item['datetime'] = node.get("datetime")
                    item['announcer'] = node.get("media_name")
                    url = node.get("item_source_url")
                    url = "https://www.toutiao.com" + url
                    item['url'] = url
                    item['attitude_count'] = 0
                    item['repost_count'] = 0
                    item['attention'] = int(item['repost_count']) + int(item['attitude_count']) + \
                                        int(item['comments_count'])
                    item['platform'] = "今日头条"
                    # 获取文章内容
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}
                    request = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(request)
                    html = str(response.read(), 'utf-8')
                    content = re.findall(r"content: '(.+);',", str(html))
                    if len(content) == 0:  # 若获取的页面为静态
                        s = etree.HTML(html)
                        content = s.xpath("//p/text()")
                        sss = ""
                        for con in content:
                            sss += con.strip()
                    else:  # 若获取的页面为动态
                        content = re.findall(u"[\u4E00-\u9FA5]|[\uFE30-\uFFA0]+", content[0])
                        sss = ""
                        for con in content:
                            sss += con.strip()
                    item['content'] = sss
                    yield item
                except:
                    pass
        if self.offset < 140:
            self.offset += 20
            url = get_page_index(self.start_url, self.offset, self.keyword)
            yield scrapy.Request(url, callback=self.parse)
