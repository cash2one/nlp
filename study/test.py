# -*- coding: utf-8 -*-
import requests

url = "http://api.nlp.baifendian.com/keywords"
data = {"contents": "自从加盟火箭队之后迈克丹尼尔斯并没有获得太多的表现机会", "num": 2, "title": "", "token": "YOUR_API_TOKEN"}
resp = requests.post(url, data=data)
print resp.text
