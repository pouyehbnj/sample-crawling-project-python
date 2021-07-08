import lxml
import re
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get


class offers(object):
    products = []
    names = []
    prices = []
    reductions = []
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
      
        
        for product in self.products:
            try:
               self.names.append(product.find("div", class_="c-product-box__img js-url js-snt-carousel_product").find('img')["alt"])
            except:

                self.names.append("No Name")
            try:
                self.prices.append(re.sub(r'\s+', ' ',product.find("div", class_="c-price__value-wrapper js-product-card-price").text))
            except:
                self.prices.append("No Price")
            try:
                self.reductions.append(product.find(
                    "div", class_="c-price__discount-oval").find("span").text)
            except:
                self.reductions.append("بدون تخفیف")

            df = pd.DataFrame({'Product Name':self.names,'Price':self.prices,'Reductions':self.reductions}) 
            df.to_csv ('products.csv', index=False,encoding='utf-8-sig')


            print(self.names[-1])
            print(self.prices[-1])
            print(self.reductions[-1])
            print("-------------------------------------------------------")

    def getNames(self):
        return self.names    
    def getPrices(self):
        return self.prices
    def getReductions(self):
        return self.reductions    


# url = "https://www.digikala.com/incredible-offers/"
# offersObj = offers(url)
# offersObj.productData()
