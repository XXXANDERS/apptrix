from decimal import Decimal

import requests
from bs4 import BeautifulSoup as BS

from products.models import Category, Product

from products.categories import categories_dict


def upload_data(url: str, parent: Category):
    name = url[:url.rfind('/')]
    name = name[name.rfind('/') + 1:]
    print(url, name, '\n')
    category_ = Category.objects.create(name=name, src=url, parent=parent)

    page = requests.get(f'{url}?p=1')
    j = 1
    while page.status_code != 404:
        j += 1

        page = requests.get(url)

        soup = BS(page.text, "html.parser")

        prices = soup.findAll('span', class_=["ProductCardVerticalPrice__price-current_current-price",
                                              "js--ProductCardVerticalPrice__price-current_current-price "])
        if not prices:
            prices = soup.findAll('span', class_=[
                "ProductCardHorizontal__price_current-price", "js--ProductCardHorizontal__price_current-price "])

        names = soup.findAll('a', class_=["ProductCardVertical__name Link js--Link Link_type_default"])
        if not names:
            names = soup.findAll('a', class_=["ProductCardHorizontal__title Link js--Link Link_type_default"])

        images = soup.findAll('img', class_=["ProductCardVertical__picture js--ProductCardInListing__picture"])
        if not images:
            images = soup.findAll('img', class_=["ProductCardHorizontal__image Image"])

        prices = [prices[i] for i in range(0, len(prices), 2)]

        # products = {}
        i = 0
        for price in prices:
            name = names[i].text.strip()
            image = images[i].attrs['src']
            try:
                d_price = Decimal(price.text.strip())
            except:
                d_price = price.text.strip()
            # products[name] = {}
            # products[name]['price'] = d_price
            # products[name]['image'] = image
            try:
                product, created = Product.objects.update_or_create(
                    name=name,
                    src=image,
                    price=d_price,
                    category=category_,
                )
            except:
                pass
            i += 1
        page = requests.get(f'{url}?p={j}')
        # print(products, '\n')


def to_parse():
    for category, data in categories_dict.items():
        print('категория', category)
        name = category[:category.rfind('/')]
        name = name[name.rfind('/') + 1:]
        parent, created = Category.objects.update_or_create(name=name, src=category)

        for cat in data:
            upload_data(cat, parent)
