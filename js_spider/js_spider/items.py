# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    note_id = scrapy.Field()
    title = scrapy.Field()
    nick_name = scrapy.Field()
    nick_id = scrapy.Field()
    likes_count = scrapy.Field()
    comments_count = scrapy.Field()
    last_updated_at = scrapy.Field()
    wordage = scrapy.Field()
    views_count = scrapy.Field()
    content = scrapy.Field()