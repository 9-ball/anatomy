import scrapy
import json

class SaavnAlbumUrl(scrapy.Spider):
    name = "saavn_album_url"                        #spider name

    start_urls = ["https://www.jiosaavn.com/new-releases/malayalam",
    "https://www.jiosaavn.com/new-releases/hindi",

    #add more urls
    ]

    headers = {
    'Cookie': 'B=7c8a2bc66828bf3736def544b8c7366b; CH=G03%2CA07%2CO00%2CL03; CT=MjAwODM3NjkzOA%3D%3D; DL=english; geo=103.123.234.246%2CIN%2CHaryana%2CPanchkula%2C134102'
    }

    def modify_url(self, url):
        url = url.strip()
        if url.startswith('//'):
            modify_url = "https:" + url
        elif url.startswith('/'):
            modify_url = "https://www.jiosaavn.com" + url
        else:
            modify_url = url
        return modify_url

    def start_requests(self):
        product_urls = self.start_urls
        for start_url in product_urls:
            yield scrapy.Request(start_url, headers=self.headers,callback=self.parse)

    def parse(self, response):
        album_url_list = []
        urls = response.xpath('//*[@class="u-centi u-margin-bottom-none@sm"]//a//@href').extract()
        for url in urls:
            album_url_json = {}
            album_url_json['url'] = self.modify_url(url)
            album_url_list.append(album_url_json)
        return album_url_list