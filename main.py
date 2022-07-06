import requests
import csv
from bs4 import BeautifulSoup
import json

url = "https://akva-mir.ru/catalog/kulery_dlya_vody/"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}

req = requests.get(url, headers=headers)
src = req.text
print(src)

with open("index.html", "w", encoding='utf-8') as file:
    file.write(src)

with open("index.html", encoding='utf-8') as file:
    src = file.read()
