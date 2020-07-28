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
        self.page = 2
        self.headers = {
                'X-CSRF-Token': 'Y9qU69H+LFxD9J1zplqZWQTxwjr+j6CwF/fKtCtyqBzCTMX4LGgLEcY/swg8ozYO0xyah0vs1RUq0jWiqor/Ew==',
                'X-INFINITESCROLL': 'true',
            }
        self.cookies = {
    "_ga":"GA1.2.258306108.1588930799",
    "__gads":"ID=d03fdd9b03bf5071:T=1588930801:S=ALNI_MZHBnUJW1VlO8sr_IE15y4rzDhdAQ",
    "__yadk_uid":"V76Xh43jzINro2VKnJP5mbvUTpXuVW5I",
    "_gid":"GA1.2.2082141055.1595774311",
    "read_mode":"day",
    "default_font":"font2",
    "locale":"zh-CN",
    "remember_user_token":"W1sxNDkxMTYyNV0sIiQyYSQxMSQ1ejg0QVBhOWNhQ2JuVnFFSUlpLnd1IiwiMTU5NTkzMzAwMi4zODEwNTIzIl0%3D--3b6914927f898e2037b376a92e634c8cda1f2f2a",
    "web_login_version":"MTU5NTkzMzAwMg%3D%3D--0e9eea2f23d5f44b42264a8395e9d544346cc800",
    "_m7e_session_core":"e87b7aef040a2d6145ad5175c82370c0",
    "Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068":"1595923117,1595923362,1595928454,1595942557",
    "sensorsdata2015jssdkcross":"%7B%22distinct_id%22%3A%2214911625%22%2C%22first_id%22%3A%22171f3a7e1d1728-0111558f062b3c-b383f66-1327104-171f3a7e1d2786%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22search-input%22%2C%22%24latest_utm_campaign%22%3A%22maleskine%22%2C%22%24latest_utm_content%22%3A%22note%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%2C%22%24device_id%22%3A%22171f3a7e1d1728-0111558f062b3c-b383f66-1327104-171f3a7e1d2786%22%7D",
    "Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068":"1595947618"
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
                cookies=self.cookies,
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
            cookies=self.cookies,
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
                cookies=self.cookies,
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
        print(self.page)
        yield item







def timestamp2string(timeStamp):
    try:
        d = datetime.datetime.fromtimestamp(timeStamp)
        str = d.strftime("%Y-%m-%d %H:%M:%S")
        # 2020-07-28 16:43:37'
        return str
    except Exception as e:
        print(e)