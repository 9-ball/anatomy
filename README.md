# Scrapy
Scrapy is a free and open-source web-crawling framework written in Python. Originally designed for web scraping, it can also be used to extract data using APIs or as a general-purpose web crawler. It is currently maintained by Zyte formerly Scrapinghub, a web-scraping development and services company.
Tutorial: https://docs.scrapy.org/en/latest/intro/tutorial.html

# Creating a project
```
scrapy startproject saavn_scraper
```

# About project (JioSaavn Scraper)
Details of newly released songs of different languages have been scraped from JioSaavn - Indian online music streaming service using Scrapy.
#### Step 1: Scrape newly released album URLs of different languages.
* Scraper: `album_url_scraper.py`
* Scraper path: `saavn_scraper/spiders/`
* Spider name: `saavn_album_url`
* Input URLs: language page URLS (eg. https://www.jiosaavn.com/new-releases/hindi)
* Output file: `saavn_albums.json`
```
scrapy crawl saavn_album_url -O saavn_albums.json
```
That will generate a `saavn_albums.json` file containing all scraped items, serialized in JSON.
#### Step 2: Scrape song URLs from album pages.
* Scraper: `song_url_scraper.py`
* Scraper path: `saavn_scraper/spiders/`
* Spider name: `saavn_song_url`
* Input URLs: album page URLS (from saavn_albums.json)
* Output file: `saavn_songs.json`
```
scrapy crawl saavn_song_url -O saavn_songs.json
```
#### Step 3: Scrape song details from song pages.
* Scraper: `song_details_scraper.py`
* Scraper path: `saavn_scraper/spiders/`
* Spider name: `saavn_song_details`
* Input URLs: song page URLS (from saavn_songs.json)
* Output file: `saavn_songs_details.json`
```
scrapy crawl saavn_song_details -O saavn_songs_details.json
```

#### Output data
`{"song_name": "Tum Na Jane Kis Jahan Men Kho Gaye", "song_duration": "3:34", "song_language": "Hindi", "album_details": {"album_name": "Sanam - Tum Na Jane Kis Jahan Men Kho Gaye", "album_url": "https://www.jiosaavn.com/album/sanam---tum-na-jane-kis-jahan-men-kho-gaye/D6lPAM3g,es_"}, "breadcrumbs": ["Home", "Albums", "Sanam - Tum Na Jane Kis Jahan Men Kho Gaye", "Tum Na Jane Kis Jahan Men Kho Gaye"], "artist_details": [{"artist_name": "Sanam (Band)", "artist_url": "https://www.jiosaavn.com/artist/sanam-band/hBK6l30Gz1w_"}, {"artist_name": "S. D. Burman", "artist_url": "https://www.jiosaavn.com/artist/s.-d.-burman/FRKH9Z9gUx4_"}, {"artist_name": "Sahir Ludhianvi", "artist_url": "https://www.jiosaavn.com/artist/sahir-ludhianvi/hel1xcytMi4_"}]}`

