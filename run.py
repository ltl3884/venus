from scrapy import cmdline
import os

spider = os.environ.get("spider")
ts = os.environ.get("ts")
sign = os.environ.get("sign")
category = os.environ.get("category")
cmd = "scrapy crawl %s" % spider
if ts:
    cmd = cmd + " -a ts=%s" % ts
if sign:
    cmd = cmd + " -a sign=%s" % sign
if category:
    cmd = cmd + " -a category=%s" % category
print(cmd.split())
cmdline.execute(cmd.split())
