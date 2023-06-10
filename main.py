import json
import re

import requests
from bs4 import BeautifulSoup
import chardet
import lxml

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

url = 'https://metaprom.ru/companies/'

"""
req = requests.get(url, headers=headers)
req.encoding = 'cp1251'
src = req.text
#print(src)

with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)
"""
with open("ind2.html", "r", encoding='cp1251') as file:
    src = file.read()
"""
soup = BeautifulSoup(src, "lxml")
all_metall_prod = soup.find_all("ul", class_="rubrics__list")
all_dict = {}
for catalog in all_metall_prod:
    rubrics = catalog.find_all("a")
    for item in rubrics:
        item_text = item.text
        ref = item.get("href")
        all_dict[item_text] = ref

with open("all_metall_prod.json", "w") as file:
    json.dump(all_dict, file, indent=4, ensure_ascii=False)
"""

with open("all_metall_prod.json", "r") as file:
    all_metall = json.load(file)

count = 0
for category_name, category_href in all_metall.items():
    if count == 0:

        """
        req = requests.get(url=category_href, headers=headers)
        req.encoding = 'cp1251'
        src = req.text

        with open(f"data/{count}_{category_name}.html", "w", encoding="cp1251") as file:
            file.write(src)
        
        with open(f"data/{count}_{category_name}.html") as file:
            src = file.read()
        """
        with open(f"data/0_Черный металлопрокат.html") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        all_firms = soup.find_all(class_="firm_name")
        firm_dict = {}
        for firm in all_firms:
            firm_text = firm.text.rstrip()
            firm_href = firm.find("a").get("href")
            firm_dict[firm_text] = firm_href

        #здесь пройти все страницы
        """
        with open("all_firms.json", "w") as file:
            json.dump(firm_dict, file, indent=4, ensure_ascii=False)
        """

        with open("all_firms.json", "r") as file:
            all_firms = json.load(file)


        firm_info_list = []

        count2 = 0
        for firm_name, firm_href in all_firms.items():

            req = requests.get(url=firm_href, headers=headers)
            req.encoding = 'cp1251'
            src = req.text

            soup = BeautifulSoup(src, "lxml")
            data = soup.find("table", class_="maintable").find("tbody").find_all("tr")

            firm_info = []
            for elem in data:
                elem_text = elem.text.replace('\n', '')
                clean_text = re.sub(r'[^\w\s.()-]', '', elem_text, flags=re.UNICODE)
                firm_info.append(clean_text)

            table_headers = ("Наименование", 'Ссылка', 'Информация')

            data_text = [firm_name, firm_href, firm_info[:-1]]
            firm_data = dict(zip(table_headers, data_text))
            firm_info_list.append(firm_data)

            count2 += 1
            print(f'Обработано: {count}.{count2}')


        firm_info_dict = {f'{count}_{category_name}': firm_info_list}
        with open(f'data/{count}_{category_name}.json', "w", encoding="cp1251") as file:
            json.dump(firm_info_dict, file, indent=4, ensure_ascii=False)

        count += 1

# компания/телефон/сайт/почта/область/город/сфера деятельности



