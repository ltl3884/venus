# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from .models import User
from .models import map_orm_item
from .models import scoped_session

class UserPipeline(object):

    def process_item(self, item, spider):
        user = User()
        user = map_orm_item(scrapy_item=item, sql_item=user)
        with scoped_session() as session:
            result = session.query(User) \
                .filter(User.user_id == str(item["user_id"])) \
                .first()
            if not result:
                session.add(user)
            else:
                logging.info("user_id:%s has already saved" % item["user_id"])
        return item