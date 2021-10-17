import requests
from bs4 import BeautifulSoup as BS

url = 'https://www.citilink.ru/catalog/smartfony-i-gadzhety/'
page = requests.get(url)
soup = BS(page.text, "html.parser")
items = soup.findAll('a', class_=['CatalogCategoryCard__link'])
# список категорий
items_dict = {}
for item in items:
    page = requests.get(item.attrs['href'])
    soup = BS(page.text, "html.parser")
    items1 = soup.findAll('a', class_=['CatalogCategoryCard__link'])

    if items1:
        items_dict[item.attrs['href']] = []
        for item1 in items1:
            items_dict[item.attrs['href']].append(item1.get('href'))


print(items_dict)
