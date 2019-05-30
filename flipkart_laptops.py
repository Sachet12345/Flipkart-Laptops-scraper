# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
import sys
import pickle
from pathlib import Path

def add_to_pickle(path, item):
	'''To add to Pickle file.'''
	with open(path, 'ab') as file:
		pickle.dump(item, file, pickle.HIGHEST_PROTOCOL)


def read_from_pickle(path):
	'''To read from the Pickle file'''
	with open(path, 'rb') as file:
		try:
			while True:
				yield pickle.load(file)
		except EOFError:
			pass

class FlipkartLaptopsSpider(scrapy.Spider):
	'''The spider class with scrapy.Spider subclass.'''
	name = 'flipkart_laptops'
	allowed_domains = ['flipkart.com']
	start_urls = ['https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off']
	#start_urls = ['https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=2']
	#count=0



	def parse(self, response):
		'''The parse method is in charge of processing the response and returning scraped data and/or more URLs to follow.'''

		#print (response.url)
		product_name=response.css('._3wU53n::text').extract()
		product_price=response.css('._1vC4OE._2rQ-NK::text').extract()
		product_rating=response.css('.hGSR34::text').extract()
		#print(product_price)
		pkl_file = sys.argv[2]
		row_data=zip(product_name,product_price,product_rating)        

		for item in row_data:
			scraped_info={
			'product-name' : item[0],
			'product_price' : item[1],
			'product-rating' : item[2],
			}
			#print("q")
			'''with open(pkl_file, 'wb') as handle:
				pickle.dump(scraped_info, handle, protocol=pickle.HIGHEST_PROTOCOL)'''
			add_to_pickle(pkl_file,scraped_info)
			yield scraped_info
			
			stats = self.crawler.stats.get_stats()
			count=stats['item_scraped_count']
			#print(count)
			#print(sys.argv[1])

			if count>=(int(sys.argv[1])-1) :
				raise CloseSpider('Limit reached')
			
			#yield scraped_info
			next_page_selector='._3fVaIS::attr(href)'
			next_page = response.css(next_page_selector).extract()
			next_page=next_page[-1]
			#print(next_page)
			print(response.urljoin(next_page))
			if next_page :
				yield scrapy.Request(response.urljoin(next_page),callback=self.parse)


process= CrawlerProcess()
process.crawl(FlipkartLaptopsSpider)
process.start()
#for item in read_from_pickle('flipkart.dat'):
		#print(repr(item))
