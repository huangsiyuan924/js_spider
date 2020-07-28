# -*- coding: utf-8 -*-
import datetime
import re

import scrapy
import json

from js_spider.items import JsSpiderItem


class JsSpider(scrapy.Spider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    def __init__(self):
        self.base_url = 'https://www.jianshu.com'
        # 文章id列表
        self.note_id_list = []
        self.params = {}
        self.page = 2
        self.headers = {
                'X-CSRF-Token': 'Y9qU69H+LFxD9J1zplqZWQTxwjr+j6CwF/fKtCtyqBzCTMX4LGgLEcY/swg8ozYO0xyah0vs1RUq0jWiqor/Ew==',
                'X-INFINITESCROLL': 'true',
            }


    def parse(self, response):
        note_list = response.xpath('//ul[@class="note-list"]//a[@class="title"]/@href').extract()
        note_id_list = response.xpath('//ul[@class="note-list"]/li/@data-note-id').extract()
        self.note_id_list.extend(note_id_list)
        next_page_url = 'https://www.jianshu.com/?'
        for note, note_id in zip(note_list, note_id_list):
            yield scrapy.Request(
                url=self.base_url + note,
                meta={"note_id": note_id},
                callback=self.parse_detail
            )
            next_page_url = next_page_url + "seen_snote_ids[]=" + note_id + "&"
        next_page_url = next_page_url + "page=" + str(self.page)
        yield scrapy.Request(
            url=next_page_url,
            meta={
                "next_page_url": next_page_url,
                "page": self.page
            },
            dont_filter=True,
            headers=self.headers,
            callback=self.next_page_parse
        )

    def next_page_parse(self, response):
        next_page_url = response.meta["next_page_url"]
        note_list = response.xpath('//a[@class="title"]/@href').extract()
        note_id_list = response.xpath('//li/@data-note-id').extract()
        next_page_url = next_page_url.split("page")[0]
        for note, note_id in zip(note_list, note_id_list):
            yield scrapy.Request(
                url=self.base_url + note,
                meta={"note_id": note_id},
                dont_filter=True,
                callback=self.parse_detail
            )
            next_page_url = next_page_url + "seen_snote_ids[]=" + note_id + "&"
        self.page += 1
        next_page_url = next_page_url + "page=" + str(self.page)
        yield scrapy.Request(
            url=next_page_url,
            meta={
                "next_page_url": next_page_url,
                "page": self.page
            },
            headers=self.headers,
            callback=self.next_page_parse
        )

    def parse_detail(self, response):

        # 当前文章页面所有数据
        all_data = json.loads(response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first())
        data = all_data["props"]["initialState"]["note"]["data"]
        # 文章id
        note_id = response.meta["note_id"]
        # 文章标题
        title = data["public_title"]
        # 作者名
        nick_name = data["user"]["nickname"]
        # 作者id
        nick_id = data["user"]["id"]
        # 赞数
        likes_count = data["likes_count"]
        # 评论数
        comments_count = data["comments_count"]
        # 帖子最后一次更新时间
        last_updated_at = timestamp2string(data["last_updated_at"])
        # 字数
        wordage = data["wordage"]
        # 阅读数
        views_count = data["views_count"]
        # 文章内容
        content = data["free_content"]
        # 去除html标签
        content = re.compile(r'<[^>]+>', re.S).sub('', content).replace("\n", "")
        item = JsSpiderItem()

        item["note_id"] = note_id
        item["title"] = title
        item["nick_name"] = nick_name
        item["nick_id"] = nick_id
        item["likes_count"] = likes_count
        item["comments_count"] = comments_count
        item["last_updated_at"] = last_updated_at
        item["wordage"] = wordage
        item["views_count"] = views_count
        item["content"] = content
        yield item







def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str = d.strftime("%Y-%m-%d %H:%M:%S")
        # 2020-07-28 16:43:37'
        return str
    except Exception as e:
        print(e)