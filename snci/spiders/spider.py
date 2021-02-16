import scrapy

from scrapy.loader import ItemLoader
from ..items import SnciItem
from itemloaders.processors import TakeFirst


class SnciSpider(scrapy.Spider):
	name = 'snci'
	start_urls = ['https://www.snci.lu/newsfeed/']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class,"texts")]')
		for post in post_links:
			date = post.xpath('./span[@class="date"]/text()').get()
			link = post.xpath("./a/@href").get()
			yield response.follow(link, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="richtext richtext1"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=SnciItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
