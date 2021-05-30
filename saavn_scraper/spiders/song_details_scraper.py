import scrapy
import json

class SaavnSongDetails(scrapy.Spider):
    name = "saavn_song_details"                       #spider name

    # custom_settings = {                           # can comment custom_settings if data is not supposed to be stored in a database 
    #     'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    #     'ITEM_PIPELINES': {
    #         'scrapy_mongodb.MongoDBPipeline': 300
    #     },
    #     'MONGODB_COLLECTION': "<database-collection-name>"
    # }

    headers = {
    'Cookie': 'B=7c8a2bc66828bf3736def544b8c7366b; CH=G03%2CA07%2CO00%2CL03; CT=MjAwODM3NjkzOA%3D%3D; DL=english; geo=103.123.234.246%2CIN%2CHaryana%2CPanchkula%2C134102'
    }

    def start_requests(self):
        with open("saavn_songs.json") as f:
            data = f.read()
        url_json_list = json.loads(data)
        urls = [url_json['url'] for url_json in url_json_list]
        urls = list(set(urls))
        for start_url in urls:
            yield scrapy.Request(start_url, headers=self.headers,callback=self.parse)

    def parse(self, response):
        data = {}
        song_name, song_time, song_lang = self.get_song_details(response)
        data['song_name'] = song_name
        data['song_duration'] = song_time
        data['song_language'] = song_lang
        data['song_url'] = response.url
        data['album_details'] = self.get_album_details(response)
        data['breadcrumbs'] = self.get_breadcrumbs(response)
        data['image'] = self.get_media(response)

        artist_info = self.get_artist_details(response)
        data['artist_details'] = artist_info
        return data

    def modify_url(self, url):
        url = url.strip()
        if url.startswith('//'):
            modify_url = "https:" + url
        elif url.startswith('/'):
            modify_url = "https://www.jiosaavn.com" + url
        else:
            modify_url = url
        return modify_url

    def get_song_details(self, response):
        song_name = response.xpath('//*[@class="u-h2 u-margin-bottom-tiny@sm"]//text()').extract()[0].replace("\u2019","'")
        song_features = response.xpath('//*[@id="root"]/div[2]//div/main//figure/figcaption//span//text()').extract()
        song_features = [feature for feature in song_features if '\xa0' not in feature]
        song_time = song_features[0]
        song_lang = song_features[1]
        return song_name, song_time, song_lang

    def get_album_details(self, response):
        album_details = {}
        album_name = response.xpath('//*[@class="u-color-js-gray-alt-light u-ellipsis@lg u-margin-bottom-tiny@sm"]//a[1]//text()').extract()[1]
        album_url = self.modify_url(response.xpath('//*[@class="u-color-js-gray-alt-light u-ellipsis@lg u-margin-bottom-tiny@sm"]//a[1]/@href').extract()[0])
        album_details['album_name'] = album_name
        album_details['album_url'] = album_url
        return album_details

    def get_artist_details(self, response):
        artist_names = response.xpath('//*[@class="o-block o-block--action o-block--rounded o-block--small"]/div[1]/a//@title').extract()
        artist_url = response.xpath('//*[@class="o-block o-block--action o-block--rounded o-block--small"]/div[1]/a//@href').extract()  
        artist_info = [{'artist_name':name,'artist_url':self.modify_url(url)} for name,url in zip(artist_names,artist_url)]
        return artist_info

    def get_breadcrumbs(self, response):
        breadcrumbs = response.xpath('//*[@id="root"]/div[2]/footer/div[1]//div/div/div/ol//text()').extract()
        breadcrumbs = [crumb.replace("\u2019","'") for crumb in breadcrumbs if crumb != ' ']  
        return breadcrumbs

    def get_media(self, response):
        image = response.xpath('//*[@class="o-flag__img u-shadow"]//img//@src').extract()[0] 
        return image        

