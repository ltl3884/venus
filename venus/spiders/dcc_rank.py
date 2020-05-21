# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from urllib.parse import urlencode, quote_plus

import scrapy
from scrapy import Request
from scrapy.utils.project import get_project_settings
from ..items import UserItem

settings = get_project_settings()

class DccRankSpider(scrapy.Spider):
    name = 'dcc_rank'
    allowed_domains = ['www.douchacha.com']
    default_headers = {
        "dcc-href": "https://www.douchacha.com/#/uppoint",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
        "Sec-Fetch-Dest": "empty",
        "TypeId": "cW1xu7",
        "Origin": "https://www.douchacha.com",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Referer": "https://www.douchacha.com/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7"
    }

    def start_requests(self):
        ts = getattr(self, "ts", "")
        he = getattr(self, "he", "w5LCjlLCml5rw4U%2BwrwRW3nDl8OCHcOWEnPCu8OOwqRqTS0%3D")
        sign = getattr(self, "sign", "")
        category = getattr(self, "category", "")
        params = {"ts": ts, "he": he, "sign": sign}
        url = "https://api.douchacha.com/api/tiktok/ranking/user_list_gain?"
        # url = "https://api.douchacha.com/api/tiktok/ranking/list_all?"
        self.default_headers["Authorization"] = settings.get("AUTHORIZATION")
        for x in range(1, 7):
            data = {"page_no":x,"page_size":100,"params_data":{"label_name":category,"period":"DAY","period_value":"20200426"}}
            yield Request(url=url + urlencode(params, quote_via=quote_plus), method="POST",
                          headers=self.default_headers, body=json.dumps(data), dont_filter=True)

    def parse(self, response):
        result = json.loads(response.body.decode("utf-8"))
        print(result)
        if result["code"] == 200:
            for user in result["data"]["result"]:
                item = UserItem()
                item["user_id"] = user["user_id"]
                item["user_name"] = user["nickname"]  # remove_html_tag.sub('',user["nickname"])
                item["unique_id"] = user.get("unique_id", "")
                item["aweme_count"] = user["aweme_count"]
                item["follower_count"] = user["follower_count"]
                item["user_score"] = int(user["user_score"])
                item["last_update_time"] = datetime.fromtimestamp(int(user["create_time"]) / 1000)
                item["source_type"] = "douyin"
                item["category"] = getattr(self, "category", "")
                item["keyword"] = "涨粉榜"
                item["share_url"] = user.get("share_url", "")
                item["avatar_larger"] = user["avatar_larger"]
                yield item
        else:
            logging.info("code:%s, msg:%s" % (result["code"], result["msg"]))
