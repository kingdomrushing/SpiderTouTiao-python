# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from TouTiao.MySqlHelperAgain import MysqlHelper

class ToutiaoPipeline(object):
    def __init__(self):
        self.f = open("theme.txt", 'w', encoding='utf-8')
        self.helper = MysqlHelper('localhost', 3306, 'test', 'root', '123456', 'utf8')
        self.helper.open()
        self.tableName = "WorldCup"
        self.platform="今日头条"
        sql="""    create table if not exists %s(
	               id int auto_increment primary key,
	               datetime varchar(20),
	               platform varchar(10),
	               announcer varchar(15),
	               theme text,
	               content text,
	               url text,
	               emotion varchar(5),
	               attitude_count varchar(20),
	               repost_count varchar(20),
	               comments_count varchar(20),
	               attention varchar(20),
	               sensitiveWords varchar(100) )
	               COLLATE='utf8_general_ci';""" % (self.tableName)
        self.helper.getCursor().execute(sql)

    def process_item(self, item, spider):
        if item['theme']!=None:
            sql = "insert into %s VALUES('%s', '%s', '%s','%s','%s','%s', '%s','%s', '%s', '%s','%s','%s')" % \
                  (self.tableName, item['datetime'], self.platform, item['announcer'], item['theme'],
                   item['content'], item['url'], None,item['attitude_count'],
                   item['repost_count'], item['comments_count'], item['attention'],None)
            self.helper.cud(sql)
            self.f.write(item['theme']+"\n")
            self.f.flush()
        return item

    def closeFile(self):
        self.helper.close()
        self.f.close()
