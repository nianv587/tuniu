# -*- coding = scrapy.Field() utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in = scrapy.Field()
# http = scrapy.Field()//doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from .settings import SQL_DATETIME_FORMAT

class HotelItem(scrapy.Item):
    acceptCreditCard = scrapy.Field()
    address = scrapy.Field()
    cashBackDesc = scrapy.Field() 
    cityCode = scrapy.Field()
    countryCode = scrapy.Field()
    debutYear = scrapy.Field()
    decorateDate = scrapy.Field()
    detailFilterArray = scrapy.Field()
    detailLottery = scrapy.Field()
    districtCode = scrapy.Field()
    districtName = scrapy.Field()
    downPaymentDesc = scrapy.Field()
    downPaymentUseRule = scrapy.Field() 
    hotelIntroduction = scrapy.Field()
    hotelLevel = scrapy.Field()
    hotelLocation = scrapy.Field()
    hotelNoticeTemplate = scrapy.Field()
    hotelPolicy = scrapy.Field()
    hotelServices = scrapy.Field()
    hotelServicesTips = scrapy.Field()
    hotelType = scrapy.Field()
    hotelZones = scrapy.Field()
    label = scrapy.Field()
    name = scrapy.Field()
    nearbyTraffic = scrapy.Field()
    newPicCount = scrapy.Field()
    pictureType = scrapy.Field()
    pictures = scrapy.Field()
    productId = scrapy.Field()
    productNum = scrapy.Field()
    productType = scrapy.Field()
    provinceCode = scrapy.Field()
    questionCount = scrapy.Field()
    scoreRemark = scrapy.Field()
    serviceAssuranceUrl = scrapy.Field()
    specialDate = scrapy.Field()
    startCity = scrapy.Field()
    strictSelectSlogan = scrapy.Field()
    tel = scrapy.Field()
    totalGrade = scrapy.Field()
    totalRemarkDesc = scrapy.Field()
    totalRemarkNum = scrapy.Field()
    totalScore = scrapy.Field()
    rooms = scrapy.Field()
