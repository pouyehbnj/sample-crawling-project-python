from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

def index(request):
    ##template = loader.get_template("index.html")
    return render(request,'/templates/products/index.html')
    ##return HttpResponse(template.render)
    ##return HttpResponse("Hello, world. You're at the crawling index.")