import lxml
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get


class offers(object):
    products = []

    def __init__(self, url):
        super(offers, self).__init__()
        page = get(url)
        self.soup = BeautifulSoup(page.content, 'lxml')

    def articleTitle(self):

        return self.soup.find("h1", class_="header").text.replace("\n", "")

    def bodyContent(self):
        content = self.soup.find(id="main")
        return content.find_all("div", class_="c-product-list__item js-product-list-content")

    def productData(self):
        self.products = self.bodyContent()
       # print(self.products[0])
        names = []
        prices = []
        reductions = []
        for product in self.products:
            try:
               names.append(product.find("div", class_="c-product-box__img js-url js-snt-carousel_product").find('img')["alt"])
            except:

                names.append("No Name")
            try:
                prices.append(re.sub(r'\s+', ' ',product.find("div", class_="c-price__value-wrapper js-product-card-price").text))
            except:
                prices.append("No Price")
            try:
                reductions.append(product.find(
                    "div", class_="c-price__discount-oval").find("span").text)
            except:
                reductions.append("No Reduction")

            df = pd.DataFrame({'Product Name':names,'Price':prices,'Reductions':reductions}) 
            df.to_csv ('products.csv', index=False,encoding='utf-8-sig')


            print(names[-1])
            print(prices[-1])
            print(reductions[-1])
            print("-------------------------------------------------------")


url = "https://www.digikala.com/incredible-offers/"
offersObj = offers(url)
offersObj.productData()
