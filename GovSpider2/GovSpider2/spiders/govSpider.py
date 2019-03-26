import scrapy
import os
import shutil
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class govSpider(CrawlSpider):

    name = "GovSpider"
    allowed_domains = ["gov.cn"]

    custom_settings = {'LOG_LEVEL': 'INFO', }

    start_urls = ["http://www.gov.cn/banshi/wjrs/crj.htm",
                  "http://www.gov.cn/banshi/wjrs/hysy.htm",
                  "http://www.gov.cn/banshi/wjrs/lssf.htm",
                  "http://www.gov.cn/banshi/wjrs/lygg.htm",
                  "http://www.gov.cn/banshi/wjrs/swtz.htm",
                  "http://www.gov.cn/banshi/wjrs/whjy.htm",
                  "http://www.gov.cn/banshi/wjrs/ymdj.htm",
                  "http://www.gov.cn/banshi/wjrs/zhjy.htm",
                  "http://www.gov.cn/banshi/wjrs/zscq.htm",
                  "http://www.gov.cn/banshi/zjpq.htm",
                  "http://www.gov.cn/banshi/wjrs/crj/wtjd.htm",
                  "http://www.gov.cn/banshi/wjrs/hysy/wtjd.htm",
                  "http://www.gov.cn/banshi/wjrs/lssf/wtjd.htm",
                  "http://www.gov.cn/banshi/wjrs/lygg/wtjd.htm",
                  "http://www.gov.cn/banshi/wjrs/swtz/wtjd.htm",
                  "http://www.gov.cn/banshi/wjrs/whjy/wtjd.htm",
                  "http://www.gov.cn/banshi/wjrs/ymdj/wtjd.htm",
                  "http://www.gov.cn/banshi/wjrs/zhjy/wtjd.htm",
                  "http://www.gov.cn/banshi/wjrs/zscq/wtjd.htm",
                  "http://www.gov.cn/banshi/zjpq_wtjd.htm"
                  ]

    links = LinkExtractor(allow="/content")

    rules = [Rule(link_extractor=links, callback='parse_item', follow=True)]

    path = os.getcwd()
    path = path + "/foregin"

    print(path)
    if not os.path.exists(path):
        os.mkdir(path)

    def parse_item(self, response):

        url = response.url
        titles = response.xpath("/html/head/title/text()").extract()
        referUrl = response.request.headers.get('Referer', None)
        referUrlStr =  str(referUrl, encoding='utf-8')
        print(titles)


        subStr = referUrlStr.rsplit('/')



        newPath = self.path
        if len(subStr) > 3:
            for i in range(len(subStr)):
                if i > 2:
                    if subStr[i].endswith(".htm"):
                        newPath = newPath + "/" + subStr[i][0:len(subStr[i])-4]

                        break
                    else:
                        newPath = newPath + "/" + subStr[i]


        newPath = newPath.strip()
        newPath = newPath.rstrip("\\")

        print(newPath)

        if titles:

            # newPath = self.path + "/haha/aa/aa"
            if not os.path.exists(newPath):
                os.makedirs(newPath)


            dirName = titles[0]
            dirName = dirName.strip()
            dirName = dirName.rstrip("\\")
            os.chdir(newPath)
            file = open(dirName + ".txt", "w")

            for sel in response.xpath("//tr"):

                title = sel.xpath("td[@class='txt18']/text()").extract()
                if title:
                    file.write(title[0] + "\n")

            for sel in response.xpath("//tr"):

                source = sel.xpath("td[@class='txt12']/text()").extract()
                if source:
                    file.write(source[0] + "\n")

            for sel in response.xpath("//tr"):

                artical = sel.xpath("td[@class='p1']/font[@id='Zoom']/p//text()").extract()
                if artical:
                    for content in artical:
                        file.write(content + "\n")

