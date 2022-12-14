import csv
import random
from time import sleep
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# url = "https://akva-mir.ru/catalog/kulery_dlya_vody/"

ua = UserAgent()  # для фейка user agent
headers = {
    "Accept": "*/*",
    "User-Agent": ua.chrome
}

# req = requests.get(url, headers=headers)
# src = req.text

# with open("index.html", "w", encoding='utf-8') as file:
#    file.write(src)

# with open("index.html", encoding='utf-8') as file:
#    src = file.read()

# soup = BeautifulSoup(src, 'lxml')

# all_coolers_href = soup.find_all(class_='catalog-top-sections__link')
# all_coolers_type_dict = {}
# for cooler_type in all_coolers_href:
#     cooler_text = cooler_type.text # название типа кулера для воды
#     if cooler_text in ["Кулеры напольные", "Кулеры настольные"]: # для парсинга только нужных типов кулеров
#         cooler_href = 'https://akva-mir.ru' + cooler_type.get('href')  # ссылка на тип кулера для воды
#         all_coolers_type_dict[cooler_text] = cooler_href

# with open('all_coolers_type_dict.json', 'w', encoding='utf-8') as file: # записываем типы кулеров в json файл
#    json.dump(all_coolers_type_dict, file, indent=4, ensure_ascii=False)


all_coolers = {
    "Кулеры напольные": "https://akva-mir.ru/catalog/kulery_napolnye/?pagecount=500",
    "Кулеры настольные": "https://akva-mir.ru/catalog/kulery_nastolnye/?pagecount=500"
}

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

for cooler_type, cooler_href in all_coolers.items():  # берёт ссылки и типы кулера из json файла
    print(f'Сейчас обрабатываются {cooler_type}')
    req = requests.get(url=cooler_href, headers=headers)
    src = req.text
    with open(f'{cooler_type}.html', 'w', encoding='utf-8') as file:
        file.write(src)
    with open(f'{cooler_type}.html', encoding='utf-8') as file:
        src = file.read()
    with open(f'data/{cooler_type}.csv', 'w', encoding='utf-8-sig') as file:  # sig нужен для правильной декодировки
        writer = csv.writer(file, delimiter=';')  # чтоб нормально разделялось
        writer.writerow(
            (
                'weight_unit : Единица веса',  # всегда кг!
                'name : Название',  # (сделано)
                'weight : Вес',  # число и есть вес (сделано)
                'article : Артикул',  # (сделано)
                'amount : Количество',  # (сделано)
                'price : Цена',  # (сделано)
                'vendor : Производитель',  # всегда AEL!
                'folder : Категория',  # cooler_type!
                'image : Иллюстрация'  # через запятую url картинок (сделано)
            )
        )
    soup = BeautifulSoup(src, 'lxml')
    all_coolers_na_hrefs = soup.find(class_="catalog-items__inner row").find_all(class_='card-image__link offer-active')
    # print(len(all_coolers_na_hrefs))

    coolers_hrefs = []  # список ссылок кулеров
    for cooler_model in all_coolers_na_hrefs:
        cooler_model_href = 'https://akva-mir.ru' + cooler_model.get('href')
        if cooler_model_href.find('600') == -1:  # исключаем тестовый кулер
            coolers_hrefs.append(cooler_model_href)

    for model in range(0, len(coolers_hrefs)):  # пробегаемя по ссылкам(пока с одним, чтоб не бомбить запросами
        print(f'Обрабатывается {model + 1}-ый кулер из категории {cooler_type}')
        req = requests.get(url=coolers_hrefs[model], headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        images = soup.find_all(class_='gallery-previews-item__image')
        cooler_images = []  # список url картинок
        for image in images:
            cooler_images.append('https://akva-mir.ru' + image.get('src') + ',')
        cooler_images_str = ""
        for i in range(0, len(cooler_images)):
            cooler_images_str += cooler_images[i]  # ЗАГРУЖАЕМ В CSV

        # print(cooler_images_str)
        title = soup.find(class_="product-title__title").text  # название модели
        name = title.strip()
        # print(name)

        article = soup.find(class_='product-number__text offer-active').text
        product_number = article.strip()  # для удаления пробелов слева и справа (артикль)
        # print(product_number)
        try:
            availabilty = soup.find(class_='product-availability__status -fullness-2').text  # проверяет на складе
            availabilty = str(random.randint(4, 11))
        except:
            availabilty = soup.find(class_='product-availability__status -fullness-0').text  # на отстутсвие
            # print(availabilty)

        try:
            price = soup.find(class_='product-prices__price -current').text
            price_rubles = price.strip().replace(' ', '').replace('₽', '')
        except:
            price_rubles = 'нет цены'

        weight = soup.find_all(class_='product-parameters__value')
        for cooler_weight in weight:
            cooler_weight_text = cooler_weight.text
            if '.' in cooler_weight_text:
                weight_netto = cooler_weight_text  # это надо заливать в CSV
                break
        # print(weight_netto)
        # print(cooler_type)
        category = ''
        if cooler_type == 'Кулеры напольные':
            category = 'Напольные кулеры для воды'
        else:
            category = 'Настольные кулеры для воды'

        with open(f'data/{cooler_type}.csv', 'a', encoding='utf-8-sig') as file:  # sig нужен для правильной декодировки
            writer = csv.writer(file, delimiter=';')  # чтоб нормально разделялось
            writer.writerow(
                (
                    'кг',  # всегда кг!
                    name,  # (сделано)
                    " " + weight_netto,  # число и есть вес (сделано). Пробел перед число для корректного вывода
                    product_number,  # (сделано)
                    availabilty,  # (сделано)
                    price_rubles,  # (сделано)
                    'AEL',  # всегда AEL!
                    f'{category}',  # cooler_type!
                    cooler_images_str  # через запятую url картинок (сделано)
                )
            )
        sleep(random.randrange(2, 4))  # задержка, чтоб не бомбить сайты
input('Работа завершена, нажмите esc')
