#https://github.com/Reljod/Python-Data-Scraping-IMDb-Movie-site-using-BeautifulSoup-Series-1-
#https://www.imdb.com/list/ls097968074/

import lxml
import re
from networkx.algorithms.distance_measures import center
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import pytextrank
import sys
sys.path.append(".")
# from compiler.ast import flatten
import matplotlib.pyplot as plt
import networkx as nx
from TextRank4Keyword import TextRank4Keyword

url1 = "https://www.imdb.com/list/ls097968074/"

class IMDB(object):
         def __init__(self, url):
                 super(IMDB, self).__init__()
                 page = get(url)
                 self.soup = BeautifulSoup(page.content, 'lxml')

         def articleTitle(self):                 
                 return self.soup.find("h1", class_="header").text.replace("\n","")

         def bodyContent(self):
                 content = self.soup.find(id="main")
                 return content.find_all("div", class_="lister-item mode-detail")

         def movieData(self):
                 movieFrame = self.bodyContent()
                 movieTitle = []
                 movieDescription = []
                 movieLink = []
                 for movie in movieFrame:
                           movieFirstLine = movie.find("h3", class_="lister-item-header")
                           movieTitle.append(movieFirstLine.find("a").text)
                       
                           movieDescription.append(movie.find_all("p", class_="")[-1].text.lstrip())
                           link = movieFirstLine.find('a')["href"]
                           movieLink.append("http://imdb.com" + link)

                        

                 movieData = [movieTitle, movieDescription , movieLink]
                 return movieData
def intersection(list1,list2):
        # a = flatten(list1)
        # b = flatten(list2)
        # common_elements = list(set(a).intersection(set(b)))
        
        return len(set(list1).intersection(set(list2)))

id1 = IMDB(url1)
#Get Article Title
print(id1.articleTitle())
#Get the first 5 movie data using for loop
#print(id1.bodyContent())
movieData = id1.movieData()
#for i in range(5):
	#print(movieData[1])
keywordLinks={}
tr4w = TextRank4Keyword()
for i in range(len(movieData[1])):
  tr4w.analyze(movieData[1][i], candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
  list=tr4w.get_keywords(5)
  keywordLinks[movieData[0][i]] = list
  print('keyword of this story line : '+str(movieData[0][i])+' '+str(list))

G = nx.Graph()

for i in keywordLinks:
        for j in keywordLinks:
                if i != j:
                        weight= intersection(keywordLinks[i] , keywordLinks[j])
                        print(weight)
                        print(i)
                        print(j)
                        G.add_edge(str(i), str(j), weight=weight)


d = nx.degree(G)
# pos=pos = nx.spring_layout(G, center='array-like',k=0.7)
# nx.draw(G, pos=pos, with_labels=True, font_weight='bold',
#         node_color="lime", font_color="red")
# plt.savefig("edge-sampling.png")
# plt.show()
pos = nx.spring_layout(G, k=0.3*1/np.sqrt(len(G.nodes())), iterations=20)
plt.figure(3, figsize=(30, 30))
nx.draw(G, pos=pos)
nx.draw_networkx_labels(G, pos=pos)
plt.show()
