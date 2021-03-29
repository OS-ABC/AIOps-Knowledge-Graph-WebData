# -*- coding: utf-8 -*-
import scrapy

class KG_spider(scrapy.Spider):
	name="KG"
	start_urls = ["https://babelnet.org/synset?word=hadoop&lang=ZH&details=1&orig=hadoop"]
	def parse(self,response):
		print(response)