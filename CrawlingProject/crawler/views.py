from django.shortcuts import render
from crawler.crawling import offers
# Create your views here.
def index(request):
    offersObj = offers("https://www.digikala.com/incredible-offers/")
    offersObj.productData()
    names = offersObj.getNames()
    prices = offersObj.getPrices()
    reductions = offersObj.getReductions()
    zipped = zip(names, prices,reductions)
    return render(request,'crawler/base.html',{"list":zipped})
    