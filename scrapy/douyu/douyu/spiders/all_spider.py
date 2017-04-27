import scrapy

class AllSpider(scrapy.Spider):
    name = "douyu_all"
    # allowed_domains = ["dmoz.org"]
    # start_urls = [
    #     "https://www.douyu.com/directory/all",
    # ]

    def start_requests(self):
        urls = [
            'https://www.douyu.com/directory/all?page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        for sel in response.xpath('/ul/li'):
            title = sel.xpath('a/text()').extract()
            print("title :" + title)
            filename = 'douyu'
            with open(filename, 'wb') as f:
                f.write(title)

