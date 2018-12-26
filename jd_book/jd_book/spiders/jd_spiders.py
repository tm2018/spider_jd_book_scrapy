#coding: utf-8
##用scrapy框架爬京东

import scrapy
import re
from selenium import webdriver
from jd_book.items import JdBookItem

#处理下获取到的url_str字符串，返回最终访问京东的合适的url
def combine_url(url_str):
    pattern = re.compile("\d+-\d+-\d+")
    cat_resoure = pattern.findall(url_str)[0]
    cat_list = cat_resoure.split("-")
    cat = ",".join(cat_list)
    tid = cat_list[-1]
    url = "%s?cat=%s&tid=%s" %('https://list.jd.com/list.html',cat,tid)
    return url

class JdSpider(scrapy.Spider):
        name = 'jd_book'
        allowed_domains = ['jd.com']
        start_urls = [
            "https://book.jd.com/booksort.html"
        ]

        def __init__(self):
            self.driver = webdriver.Firefox()
            self.driver.set_page_load_timeout(30)
        def parse(self,response):
                for sel in response.xpath('//*[@id="booksort"]/div[@class="mc"]/dl/dd/em'):
                        item = JdBookItem()
                        item['nav2_name'] = sel.xpath('a/text()').extract()[0]
                        relate_url = sel.xpath('a/@href').extract()[0]
                        nav2_url = combine_url(relate_url)
                        item['nav2_url'] = nav2_url
                        yield scrapy.Request(nav2_url,callback=self.book_parse,meta={'item':item})
        def book_parse(self,reponse):
                self.driver.get(reponse.url)


                # for sel in reponse.xpath('//*[@id="plist"]/ul/li/div'):
                #     print sel.xpath('div[@class="p-price"]/strong[@class="J_price"]/i').extract()

