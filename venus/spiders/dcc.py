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


class DccSpider(scrapy.Spider):
    name = 'dcc'
    allowed_domains = ["www.douchacha.com"]
    default_headers = {
        "dcc-href": "https://www.douchacha.com/#/searchdetail?from=search&type=vip&isShop=person",
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
        # cs = {"篮球": 300, "库里": 50, "哈登": 50, "詹姆斯": 50, "科比": 50, "奥尼尔": 15,
        #                 "姚明": 30, "杜兰特": 20, "诺维斯基": 10, "韦德": 10, "字母哥": 10, "约基奇": 10,
        #                 "东契奇": 10, "保罗乔治": 10, "莱昂纳德": 10, "凯里欧文": 10, "威少": 10, "nba": 30,
        #                 "湖人": 10, "勇士": 10, "雄鹿": 5, "凯尔特人": 5, "76人": 5, "快船": 5, "火箭": 5,
        #                 "独行侠": 5, "掘金": 5, "雷霆": 5}
        # cs = {"电影解说": 100}
        # cs = {"生活技巧": 30}
        cs = {"开箱": 100}
        params = {"ts": ts, "he": he, "sign": sign}
        url = "https://api.douchacha.com/api/tiktok/search/user?"
        self.default_headers["Authorization"] = settings.get("AUTHORIZATION")
        for keyword, size in cs.items():
            if size > 100:
                for x in range(1, int(size / 100) + 1):
                    data = self.post_data(x, keyword, size)
                    yield Request(url=url + urlencode(params, quote_via=quote_plus), method="POST",
                                  headers=self.default_headers, body=json.dumps(data), dont_filter=True,
                                  meta={"keyword": keyword})
            else:
                data = self.post_data(1, keyword, size)
                yield Request(url=url + urlencode(params, quote_via=quote_plus), method="POST",
                              headers=self.default_headers, body=json.dumps(data), dont_filter=True,
                              meta={"keyword": keyword})

    def post_data(self, page_no, keyword, page_size):
        page_size = 100 if page_size >= 100 else page_size
        data = {"page_no": page_no, "page_size": page_size,
                "params_data": {"is_verified": "ALL", "is_gov_media_vip": "ALL",
                                "with_fusion_shop_entry": "ALL",
                                "follower_count": "ALL", "total_favorited": "ALL", "aweme_count": "ALL",
                                "goods_count": "ALL", "sex_flag": "ALL", "age": "ALL", "city": "",
                                "city_flag": "",
                                "sex": "ALL", "age_flag": "ALL", "selectedOptions": [],
                                "dSelectedOptions": [],
                                "constellation": "-1", "constellation_flag": "-1", "province": "",
                                "province_flag": "",
                                "keyword": keyword, "user_tag": "", "sort": "FOLLOWER"}}
        return data

    def parse(self, response):
        # remove_html_tag = re.compile('</?\w+[^>]*>')
        result = json.loads(response.body.decode("utf-8"))
        if result["code"] == 200:
            for user in result["data"]["result"]:
                item = UserItem()
                item["user_id"] = user["user_id"]
                item["user_name"] = user["nickname"]  # remove_html_tag.sub('',user["nickname"])
                item["unique_id"] = user["unique_id"]
                item["aweme_count"] = user["aweme_count"]
                item["follower_count"] = user["follower_count"]
                item["user_score"] = int(user["user_score"])
                item["last_update_time"] = datetime.fromtimestamp(int(user["last_update_time"]) / 1000)
                item["source_type"] = "douyin"
                item["category"] = getattr(self, "category", "")
                item["keyword"] = response.meta["keyword"]
                item["share_url"] = user["share_url"]
                item["avatar_larger"] = user["avatar_larger"]
                yield item
        else:
            logging.info("code:%s, msg:%s" % (result["code"], result["msg"]))
