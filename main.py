import requests
import csv
from bs4 import BeautifulSoup
import json

#url = "https://akva-mir.ru/catalog/kulery_dlya_vody/"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}

#req = requests.get(url, headers=headers)
#src = req.text

#with open("index.html", "w", encoding='utf-8') as file:
#    file.write(src)

#with open("index.html", encoding='utf-8') as file:
#    src = file.read()

#soup = BeautifulSoup(src, 'lxml')

# all_coolers_href = soup.find_all(class_='catalog-top-sections__link')
# all_coolers_type_dict = {}
# for cooler_type in all_coolers_href:
#     cooler_text = cooler_type.text # название типа кулера для воды
#     if cooler_text in ["Кулеры напольные", "Кулеры настольные"]: # для парсинга только нужных типов кулеров
#         cooler_href = 'https://akva-mir.ru' + cooler_type.get('href')  # ссылка на тип кулера для воды
#         all_coolers_type_dict[cooler_text] = cooler_href

#with open('all_coolers_type_dict.json', 'w', encoding='utf-8') as file: # записыввем типы кулеров в json файл
#    json.dump(all_coolers_type_dict, file, indent=4, ensure_ascii=False)

with open('all_coolers_type_dict.json', encoding='utf-8') as file: #ссылки на типы кулеров по 500 страниц
    all_coolers = json.load(file)

# for cooler_type, cooler_href in all_coolers.items(): #берёт ссылки и типы кулера из json файла
#     req = requests.get(url=cooler_href, headers=headers)
#     src = req.text
#     with open(f'data/{cooler_type}.html', 'w', encoding='utf-8') as file:
#         file.write(src)
#     with open(f'data/{cooler_type}.html', encoding='utf-8') as file:
#         src = file.read()
#     soup = BeautifulSoup(src, 'lxml')
#     all_coolers_species_href = soup.find_all(class_='catalog-top-sections__link')
#     all_coolers_type_species_dict = {} # словарь видов типа кулеров
#     for cooler_species_type in all_coolers_species_href:
#         cooler_species_text = cooler_species_type.text  # название типа кулера для воды  # для парсинга только нужных типов кулеров
#         cooler_species_href = 'https://akva-mir.ru' + cooler_species_type.get('href') + '?pagecount=500'  # ссылка на тип кулера для воды
#         all_coolers_type_species_dict[cooler_species_text] = cooler_species_href
#     with open(f'all_coolers_{cooler_type}_dict.json', 'w', encoding='utf-8') as file:  # записыввем типы кулеров в json файл
#         json.dump(all_coolers_type_species_dict, file, indent=4, ensure_ascii=False)


