from scrapy.selector import Selector
from scrapy.spiders import Spider
import scrapy


# from scrapy.douban_new_movie.douban_new_movie.items import DoubanNewMovieItem

class DoubanNewMovieSpider(Spider):
    name = 'douban_new_movie_spider'

    allowed_domains = ["www.movie.douban.com"]

    def start_requests(self):
        start_urls = [
            'http://movie.douban.com/chart'
        ]
        for url in start_urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        movie_name = sel.xpath("//div[@class='pl2']/a/text()[1]").extract()
        movie_url = sel.xpath("//div[@class='pl2']/a/@href").extract()
        movie_star = sel.xpath("//div[@class='pl2']/div/span[@class='rating_nums']/text()").extract()

        # item = DoubanNewMovieItem()
        item = {}
        # item['movie_name'] = [n.encode('utf-8') for n in movie_name]
        item['movie_name'] = movie_name
        item['movie_star'] = [n for n in movie_star]
        item['movie_url'] = [n for n in movie_url]

        yield item

        print(item['movie_name'], item['movie_star'], item['movie_url'])
