# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookdepositItem(scrapy.Item):
    BookURL = scrapy.Field()
    ImageURL = scrapy.Field()
    Format = scrapy.Field()
    Dimensions = scrapy.Field()
    Weight = scrapy.Field()
    Pubdate = scrapy.Field()
    Publisher = scrapy.Field()
    Language = scrapy.Field()
    Illustrationsnote = scrapy.Field()
    ISBN10 = scrapy.Field()
    ISBN13 = scrapy.Field()
    Bestsellersrank = scrapy.Field()
    Title = scrapy.Field()
    FullDesc = scrapy.Field()
    stock = scrapy.Field()
    Price = scrapy.Field()
    Author = scrapy.Field()
    Category = scrapy.Field()

