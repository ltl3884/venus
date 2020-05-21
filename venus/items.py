# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    unique_id = scrapy.Field()
    aweme_count = scrapy.Field()
    follower_count = scrapy.Field()
    user_score = scrapy.Field()
    last_update_time = scrapy.Field()
    source_type = scrapy.Field()
    category = scrapy.Field()
    keyword = scrapy.Field()
    share_url = scrapy.Field()
    avatar_larger = scrapy.Field()