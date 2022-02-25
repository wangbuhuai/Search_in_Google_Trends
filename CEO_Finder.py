# Created by Dayu Wang (dwang@stchas.edu) on 2022-02-25

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-02-25


import requests
import json

c2coff = 1
hl = "en"
lr = "lang_en"
key = "AIzaSyDt_OsC0qcvbr1dCrXFihbWuWAXDWpGAkY"
cx = "8ed8195879518fa37"
q = "3M Company CEO".replace(' ', "%20").replace('&', "%26")

response = requests.get("https://www.googleapis.com/customsearch/v1?c2coff=%dhl=%s&lr=%s&key=%s&cx=%s&q=%s" % (
    c2coff, hl, lr, key, cx, q
))

result = json.loads(response.text)
print(response.text)

