# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    theme = scrapy.Field()
    comments_count=scrapy.Field()
    url=scrapy.Field()
    content = scrapy.Field()
    datetime=scrapy.Field()
    announcer=scrapy.Field()
    attitude_count = scrapy.Field()
    repost_count = scrapy.Field()
    attention=scrapy.Field()
    # pass
