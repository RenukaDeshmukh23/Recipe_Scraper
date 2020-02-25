# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class RecipeSpider(scrapy.Spider):
    name = 'recipe'
    allowed_domains = ['yummly.com']
    start_urls = ['http://yummly.com/recipes?q=vegan']

    def parse(self, response):
        Links= response.xpath('//*[@class="card-info primary-dark"]/a/@href').extract()
        for Link in Links:
            Link=response.urljoin(Link)
            #yield{'url':Link}
            yield Request(Link,callback=self.parse_recipe,
                            meta={'href':Link})


    def parse_recipe(self,response):
        recipe_name=response.xpath('//*[@class="recipe-title font-bold h2-text primary-dark"]/text()').extract()
        #recipe_img=response.xpath('//img/@src').extract()[4]
        ing= response.xpath('//*[@class="summary-item-wrapper"]//text()').extract_first()
        Time=response.xpath('//*[@class="summary-item-wrapper"]//text()').extract()[2]
        Directions=response.xpath('//*[@class="read-dir-btn btn-primary wrapper recipe-summary-full-directions p1-text"]/@href').extract()
        if "#directions"==Directions:
            Directions=response.meta['href']
            
        Ingredients=response.xpath('//*[@class="shopping-list-ingredients"]//li')
        for ingredient in Ingredients:
            #amount=Ingredients.xpath('.//*[@class="amount"]//text() |' './/*[@class="ingredient"]//text()').extract()
            amount=Ingredients.xpath('.//*[@class="amount"]//text() |'
            './/*[@class="ingredient"]//text()').extract()
        Nutrition=response.xpath('//*[@class="recipe-nutrition"]')
        for value in Nutrition:
            Calories=Nutrition.xpath('.//text()').extract()[0]
            Sodium=Nutrition.xpath('.//text()').extract()[3]
            Fat=Nutrition.xpath('.//text()').extract()[6]

        yield{'recipe name':recipe_name,
        #    'Recipe Image':recipe_img,
            'total # of ingredients':ing,
            'total time to make(in minutes)':Time,
            'link to directions':Directions,
            'list of ingredients':amount,
            'Calories':Calories,
            'Sodium':Sodium,
            'Fat':Fat
            }
