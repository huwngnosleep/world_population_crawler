import scrapy


class WorldometerSpider(scrapy.Spider):
    base_url = 'https://www.worldometers.info'
    name = 'worldometer'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/population/']

    def parse(self, response):
        countries = response.xpath('(//ul)[10]/li/a')
        
        for country in countries:
            name = country.xpath(".//text()").get()
            url = country.xpath(".//@href").get()

            yield scrapy.Request(url=self.base_url + url, callback=self.parse_country, meta={'country_name': name})

    def parse_country(self, response):
        name = response.request.meta["country_name"]
        
        country_data = response.xpath(
            "//table[@class='table table-striped table-bordered table-hover table-condensed table-list']/tbody/tr")

        for year in country_data:
            year_data = year.xpath('.//td')
            yield {
                'name': name,
                'year': year_data[0].xpath('./text()').get(),
                'population': year_data[1].xpath('./strong/text()').get(),
                'yearly_change_percent': year_data[2].xpath('./text()').get(),
                'yearly_change': year_data[3].xpath('./text()').get(),
                'migrants': year_data[4].xpath('./text()').get(),
                'median_age': year_data[5].xpath('./text()').get(),
                'fertility_rate': year_data[6].xpath('./text()').get(),
                'people_per_km_square': year_data[7].xpath('./text()').get(),
                'urban_population_percent': year_data[8].xpath('./text()').get(),
                'urban_population': year_data[9].xpath('./text()').get(),
                'shape_of_world_percent': year_data[10].xpath('./text()').get(),
            }
