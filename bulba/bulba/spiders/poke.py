import scrapy

class PokeSpider(scrapy.Spider):
	name = 'poke'
	start_urls = ['https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pok%C3%A9mon)']

	def parse(self, response):
		eng_name = response.xpath('//b/text()').extract()[0]
		jap_name = response.xpath('//p/b/text()').extract()[1]
		poke_id = response.xpath('//span[@style="color:#000;"]/text()').extract()[6]
		img_url = 'https:' + response.xpath('//a[@class="image"]/img/@src').extract()[0]
		yield {
			'question': str(img_url),
			'answers': [str(eng_name), str(jap_name)],
			'comment': str(poke_id)
		}
		next_page = 'https://bulbapedia.bulbagarden.net' + response.xpath('//td[@style="text-align: left"]/a/@href').extract()[0]
		#print(str(next_page))
		till_page = 'https://bulbapedia.bulbagarden.net/wiki/Chikorita_(Pok%C3%A9mon)'
		if str(next_page) != till_page:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
