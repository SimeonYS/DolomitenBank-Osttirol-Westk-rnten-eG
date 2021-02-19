import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import DolomitenItem

pattern = r'(\r)?(\n)?(\t)?(\xa0)?'


class SpiderSpider(scrapy.Spider):
    name = 'spider'

    start_urls = ['https://www.dolomitenbank.at/news']

    def parse(self, response):
        links = response.xpath('//a[@class="read-more"]/@href').getall()

        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(DolomitenItem())
        item.default_output_processor = TakeFirst()

        title = ' '.join(response.xpath('//div[@class="box_header"]/h1//text()').getall())
        content = response.xpath('//div[@class="textbox"]//text()').getall()
        content = [text.strip() for text in content if text.strip()]
        content = re.sub(pattern, "", ' '.join(content))
        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()