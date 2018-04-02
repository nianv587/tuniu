# -*- coding: utf-8 -*-
import scrapy
import json
# import re
# from scrapy_splash import SplashRequest
# from urllib import parse
# from datetime import datetime
from tuniu.items import HotelItem
class FlightsSpider(scrapy.Spider):
    name = 'hotel'
    # start_urls = ['http://flight.tuniu.com/timetable/']
    text_city = '602'
    text_checkin = '2018-03-31'
    text_checkout = '2018-04-1'
    hotel_lists = 'http://hotel.tuniu.com/ajax/list?search%5Bcity%5D={city_code}&search%5BcheckInDate%5D={check_in_date}&search%5BcheckOutDate%5D={check_out_date}&search%5BcityCode%5D={city_code}&page={page}'
    hotel_room = 'http://hotel.tuniu.com/ajax/hotelRooms?id={hotel_id}&checkindate={check_in_date}&checkoutdate={check_out_date}'
    hotel_static = 'http://hotel.tuniu.com/ajax/getHotelStaticInfo?id={hotel_id}&checkindate={check_in_date}&checkoutdate={check_out_date}'
    mhotel_lists = 'https://m.tuniu.com/api/hotel/product/hotelList?d=%7B%22page%22%3A1%2C%22limit%22%3A30000%2C%22cityCode%22%3A{city_code}%2C%22checkInDate%22%3A%22{check_in_date}%22%2C%22checkOutDate%22%3A%22{check_out_date}%22%7D'
    mhotel_room ='https://m.tuniu.com/api/hotel/product/hotelRoomRatePlanM?d=%7B%22productId%22%3A{hotel_id}%2C%22checkInDate%22%3A%22{check_in_date}%22%2C%22checkOutDate%22%3A%22{check_out_date}%22%7D'
    mhotel_static = 'https://m.tuniu.com/api/hotel/product/hotelStaticInfo?d=%7B%22productId%22%3A{hotel_id}%7D'
    # https: // m.tuniu.com / api /hotel/product/hotelStaticInfo?d=%7B%22productId%22%3A394573%7D
    custom_settings = {
        "COOKIES_ENABLED": True,
        # "DOWNLOAD_DELAY": 0.5,
        # "RANDOMIZE_DOWNLOAD_DELAY": True,
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
            'Cache - Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Content-Length': '0',
            'Cookie': 'hotel_user_token=F2AF9A0E5E3BA0A547D4B992A5F97898; hotel_checkin_date=2018-03-29; hotel_checkout_date=2018-03-30; page_flag=; _tacau=MCxhYzUxYzIwNS1hNGMyLTIxYzktMzhhNS1jZDY4ZTFmZTFlZjks; _tact=YWY5NWE0NjAtNDJmOC1iZTBkLWJkY2EtYjNjZjI4ODNmNGVi; _tacz2=taccsr%3D%28direct%29%7Ctacccn%3D%28none%29%7Ctaccmd%3D%28none%29%7Ctaccct%3D%28none%29%7Ctaccrt%3D%28none%29; _taca=1522332392436.1522332392436.1522332392436.1; _tacb=OTc1M2FhNTAtN2I5OS1mYmRjLTBmNTYtYjczOTg2Y2MzZDI0; _tacc=1; appDownload=200; tuniu_partner=MjAxLDAsLGQzN2UwNjg4ZDEyYzVmMmNmYzBlYjMyZGUyMzFkMDQ5; tuniuuser_citycode=NjAy; __utma=1.636143075.1522332393.1522332393.1522332393.1; __utmc=1; __utmz=1.1522332393.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=1.1.10.1522332393',
            'Host': 'm.tuniu.com',
            # 'Origin': 'http://hotel.tuniu.com',
            'Upgrade - Insecure - Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
    }

    def start_requests(self):
        #根据城市编号构造要爬取的城市所有酒店列表的api
        yield scrapy.Request(
            url=self.mhotel_lists.format(
                city_code=self.text_city, check_in_date=self.text_checkin, check_out_date=self.text_checkout),
            callback=self.city_list, meta={'city_code': self.text_city}
            )

    def city_list(self, response):
        #从某城市的所有酒店list里提取每个酒店的hotel_id，然后使用hotel_id构造每个酒店的房间详细信息的api
        city_code = response.meta['city_code']
        result = json.loads(response.text)
        for i in result['data']['rows']:
            hotel_id = i['hotelId']
            yield scrapy.Request(
                url=self.mhotel_room.format(hotel_id=hotel_id, check_in_date=self.text_checkin, check_out_date=self.text_checkout),
                callback=self.room_info,
                meta={'hotel_id': hotel_id}
            )
        #以下为测试翻页代码
        # total_page = int(result['data']['page']['total'])
        # current_page = int(result['data']['page']['current'])
        # if current_page != total_page:
        #     current_page += 1
        #     next_url = self.hotel_lists.format(
        #         city_code=response.meta['city_code'], check_in_date=self.text_checkin,
        #         check_out_date=self.text_checkout, page=current_page
        #     )
        #     yield scrapy.Request(url=next_url, callback=self.city_list, meta={'city_code': response.meta['city_code']})

    def room_info(self, response):
        #根据hotel_id获取该酒店房间详细信息后，再构造酒店的基本信息api，并把房间详细信息传递到酒店基本信息处理的函数里
        hotel_id = response.meta['hotel_id']
        result = json.loads(response.text)
        rooms = {}
        # if result['data']:
        for i in result['data']:
            rooms[i['name'].replace('.', '_')] = i
        yield scrapy.Request(
                url=self.mhotel_static.format(hotel_id=hotel_id, check_in_date=self.text_checkin, check_out_date=self.text_checkout),
                callback=self.hotel_info, meta={'room_item': rooms})
        # else:
        #     print(result['data'])

    def hotel_info(self, response):
        #根据hotel_id获取到酒店基本信息，再合并酒店的房间信息成一个item，然后通过yield给pipelines转存到MongoDB
        result = json.loads(response.text)
        a = result['data']
        item = HotelItem()
        for field in item.fields:
            if field in a.keys():
                item[field] = a.get(field)
        item['rooms'] = response.meta['room_item']
        yield item