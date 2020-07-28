# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from js_spider.mysqlUtil import MysqlHelper


class JsSpiderPipeline(object):
    def __init__(self):
        self.helper = MysqlHelper()
    def process_item(self, item, spider):
        note_id = item["note_id"]
        title = item["title"]
        nick_name = item["nick_name"]
        nick_id = item["nick_id"]
        likes_count = item["likes_count"]
        comments_count = item["comments_count"]
        last_updated_at = item["last_updated_at"]
        wordage = item["wordage"]
        views_count = item["views_count"]
        content = item["content"]
        self.helper.insert_js_spider(note_id,
                                     title,
                                     nick_name,
                                     nick_id,
                                     likes_count,
                                     comments_count,
                                     last_updated_at,
                                     wordage,
                                     views_count,
                                     content)
        return item
