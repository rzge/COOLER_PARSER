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

with open("index.html", "w", encoding='utf-8') as file:
    file.write(src)

with open("index.html", encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

all_coolers_href = soup.find_all(class_='catalog-top-sections__link')
for cooler_type in all_coolers_href:
    cooler_text = cooler_type.text # название типа кулера для воды
    cooler_href = 'https://akva-mir.ru' + cooler_type.get('href') #ссылка на тип кулера для воды
    print(cooler_text + ' ' + cooler_href)