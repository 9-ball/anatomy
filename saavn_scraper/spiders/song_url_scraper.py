import scrapy
import json

class SaavnSongUrl(scrapy.Spider):
    name = "saavn_song_url"

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
        with open("saavn_albums.json") as f:                #read scraped album URLs
            data = f.read()
        url_json_list = json.loads(data)
        urls = [url_json['url'] for url_json in url_json_list]
        urls = list(set(urls))
        for start_url in urls:
            yield scrapy.Request(start_url, headers=self.headers,callback=self.parse)

    def parse(self, response):
        song_url_list = []
        urls = response.xpath('//*[@class="o-flag__body"]//h4/a//@href').extract()
        for url in urls:
            song_url_json = {}
            song_url_json['url'] = self.modify_url(url)
            song_url_list.append(song_url_json)
        return song_url_list
