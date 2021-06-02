import scrapy
from scrapy import Request

class PulpSpider(scrapy.Spider):
    name = "hollywood"

    start_urls = [
        'https://www.rottentomatoes.com/m/once_upon_a_time_in_hollywood/reviews?intcmp=rt-what-to-know_read-critics-reviews',
    ]

    def parse(self, response):
        for review in response.css('div.review_table_row'):
            yield {
                'review_text': review.css('div.the_review::text').get()
            }
        
        next_page = response.css('a.btn-primary-rt::attr(href)')[1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
