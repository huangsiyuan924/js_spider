'''
-*- coding: utf-8 -*-
@Author  : Haxp
@Time    : 28/07/2020 10:18 PM
@Software: PyCharm
@File    : mysqlUtil.py
@Email   : huangsiyuan924@gmail.com
'''
import json

import pymysql





class MysqlHelper():

    def __init__(self):
        # 连接MySQL
        self.db = pymysql.connect("localhost", "root", "asdasdasd", "test")
        # 创建cursor对象
        self.cursor = self.db.cursor()

        self.cursor.execute('''
                        CREATE TABLE IF NOT EXISTS js_spider(
                        note_id INT PRIMARY KEY, -- 文章id
                        title VARCHAR(150) NOT NULL, -- 文章标题
                        nick_name VARCHAR(30) NOT NULL, -- 作者名
                        nick_id INT NOT NULL, -- 作者id
                        likes_count INT NOT NULL, -- 赞数
                        comments_count INT NOT NULL, -- 评论数
                        last_updated_at DATETIME NOT NULL, -- 帖子最后一次更新时间
                        wordage INT NOT NULL, -- 字数
                        views_count INT NOT NULL, -- 阅读数
                        content TEXT NOT NULL, -- 文章内容
                        )
        ''')

    def insert_js_spider(self,
                         note_id,
                         title,
                         nick_name,
                         nick_id,
                         likes_count,
                         comments_count,
                         last_updated_at,
                         wordage,
                         views_count,
                         content):
        sql = "INSERT INTO qsbk(note_id, title, nick_name, nick_id, likes_count, comments_count, last_updated_at, wordage, views_count, content) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (note_id, title, nick_name, nick_id, likes_count, comments_count, last_updated_at, wordage, views_count, content)
        self.cursor.execute(sql)
        self.db.commit()
    def close(self):
        self.db.close()




def test():
    pass
    # helper = MysqlHelper()
    # helper.cursor.execute("SELECT comments_list FROM qsbk")
    # mydata = helper.cursor.fetchall()
    # for i in range(len(mydata)):
    #     datas = json.loads(mydata[i][0], encoding='utf-8', strict=False)
    #     for data in datas:
    #         print(data[0] + ": " + data[1])
    #     print("*" * 40)
if __name__ == '__main__':
    test()