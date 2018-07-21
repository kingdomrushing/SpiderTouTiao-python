# -*- coding: utf-8 -*-
import scrapy
import json
from TouTiao.items import ToutiaoItem
from urllib.parse import urlencode
from selenium import webdriver


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

class JinritoutiaoSpider(scrapy.Spider):
    name = 'JinRiTouTiao'
    allowed_domains = ['toutiao.com']
    keyword="世界杯"
    offset=0
    start_url = 'https://www.toutiao.com/search_content/?'
    url = get_page_index(start_url,offset,keyword)
    start_urls = [url]

    def parse(self, response):
        dic = json.loads(response.text)
        if dic and 'data' in dic.keys():
            for node in dic.get('data'):
                item = ToutiaoItem()
                try:
                    item['theme'] = node.get("title")
                    item['comments_count'] = node.get("comments_count")
                    item['url'] = node.get("article_url")
                    driver = webdriver.PhantomJS()
                    driver.get(node.get("article_url"))
                    data = driver.find_elements_by_xpath("//p")
                    text = "".join([d.text.strip() for d in data])
                    item["content"] = text
                    item['datetime'] = node.get("datetime")
                    item['announcer'] = node.get("media_name")
                    item['attitude_count'] = 0
                    item['repost_count'] = 0
                    item['attention'] = int(item['repost_count']) + int(item['attitude_count']) + int(
                        item['comments_count'])
                    yield item
                except:
                    pass
        if self.offset < 140:
            self.offset += 20
            url = get_page_index(self.start_url, self.offset, self.keyword)
            yield scrapy.Request(url, callback=self.parse)


