#coding: utf-8
##用scrapy框架爬京东

import scrapy
import re
from selenium import webdriver
from jd_book.items import JdBookItem
from urlparse import urlparse

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
        #用spider的默认方式访问图书全部分类页面,获取到每个分类的地址并访问
        def parse(self,response):
                for sel in response.xpath('//*[@id="booksort"]/div[@class="mc"]/dl/dd/em'):
                        relate_url = sel.xpath('a/@href').extract()[0]
                        nav2_url = combine_url(relate_url)
                        #访问每个分类的url
                        yield scrapy.Request(nav2_url,callback=self.book_nav2_parse)

        # 访问分类url的方法
        def book_nav2_parse(self,reponse):
                for blank_url in reponse.xpath('//*[@id="plist"]/ul/li//*/div[@class="p-img"]/a/@href').extract():
                    #组合成真实的url
                    book_url = "%s%s" %("https:", blank_url)
                    print '11111111111111111%s' % book_url
                    yield scrapy.Request(book_url,callback=self.book_parse)

        #这里地址是'https://item.jd.com/'类型的，在middlewares.py中判断了，会重写访问方式---selenium
        def book_parse(self,reponse):
                print "2222222222222222222222222222222222222222222"
                # #设置和写入item
                html = url
                # item = JdBookItem()
                # item['book_name'] = "333333333333333333"
                # print 333333
                # # # from scrapy.shell import inspect_response
                # # # inspect_response(reponse,self)
                # #
                # #xpath取各种值
                # book_itemInfo = reponse.xpath('//*[@id="itemInfo"]')
                # book_name = book_itemInfo.xpath('//*[@class="sku-name"]').extract()[0]
                # book_price = book_itemInfo.xpath('//*[@class="p-price"]').extract()[0]
                #
                # book_introduction = reponse.xpath('//*[@id="parameter2"]')
                # book_publishing_house = book_introduction.xpath('li[contains(@title,"出版社")]/a/text()').extract()[0]
                # book_publishing_time = book_introduction.xpath('//*[@id="parameter2"]/li[contains(text(),"出版时间")]//../@title').extract()[0]
                # book_edition = book_introduction.xpath('//*[@id="parameter2"]/li[contains(text(),"版次")]//../@title').extract()[0]
                # # item["book_name"] = book_name
                # yield item




