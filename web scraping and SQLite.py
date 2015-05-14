
# coding: utf-8

# In[150]:

import sqlite3
import urllib
import pandas
from bs4 import BeautifulSoup
import time
import re


# In[151]:

newinurl = {}; soups={}; asostemp=[[],[],[]];zaratemp=[[],[],[]];topshoptemp=[[],[],[]];temp=[]


# In[152]:

asos = urllib.urlopen("http://www.asos.com/Women/").read();
#zara = urllib.urlopen("http://www.zara.com/sg/").read();
topshop = urllib.urlopen("http://sg.topshop.com/en").read()


# In[153]:

soupasos = BeautifulSoup(asos,"html.parser");
#soupzara = BeautifulSoup(zara,"html.parser");
souptopshop = BeautifulSoup(topshop,"html.parser")


# In[154]:

#get to the new in page
a = soupasos.find("ul", class_="items").find("a")
#z = soupzara.find("ul", id="mainNavigationMenu").find_all("li")[0].find("a")
#z1 = soupzara.find("ul", id="mainNavigationMenu").find_all("li")[3].find("a")
t = souptopshop.find("li", class_="category_737001").find("a")
newinurl['asos'] = a.get('href')
newinurl['zara'] = "http://www.zara.com/sg/en/new-this-week/woman-c363008.html"
newinurl['topshop'] = t.get('href')
for shop in newinurl:
    print shop
    print newinurl[shop]


# In[155]:

for shop in newinurl:
    if shop == "asos":
        sites = urllib.urlopen(newinurl[shop]).read()
        soup = BeautifulSoup(sites,"html.parser")
        for i in soup.find_all("a",class_="desc"):
            asostemp[1].append(i.getText())
            asostemp[0].append(time.strftime("%d/%m/%Y"))
        for i in soup.find_all("div",class_="productprice"):
            asostemp[2].append(i.getText().strip().encode("ascii",'ignore').split()[-1])
    
    elif shop == "topshop":
        sites = urllib.urlopen(newinurl[shop]).read()
        soup = BeautifulSoup(sites,"html.parser")
        for i in soup.find_all("li", class_ = "product_description"):
            topshoptemp[1].append(i.getText())
            topshoptemp[0].append(time.strftime("%d/%m/%Y"))
        for i in soup.find_all("li", class_ = "product_price"):
            topshoptemp[2].append(i.getText()[4:])
    
    elif shop == "zara":
        sites = urllib.urlopen(newinurl[shop]).read()
        soup = BeautifulSoup(sites,"html.parser")
        for i in soup.find_all("a",class_="name item"):
            zaratemp[1].append(i.getText())
            zaratemp[0].append(time.strftime("%d/%m/%Y"))
        for i in soup.find_all("span"):
            m = re.search('data-ecirp',repr(i.span))
            if m:
                n = repr(i.span).split("\"")
                zaratemp[2].append(n[1])


# In[172]:

print 'shop','\ttime','\tname','\tprice'
print 'asos\t',len(asostemp[0]), '\t',len(asostemp[1]), '\t',len(asostemp[2])
print 'topshop\t',len(topshoptemp[0]), '\t',len(topshoptemp[1]), '\t',len(topshoptemp[2])
print 'zara\t',len(zaratemp[0]), '\t',len(zaratemp[1]),'\t', len(zaratemp[2])


# In[157]:

asosdf = pandas.DataFrame({'time' :asostemp[0], 
                           'Name':asostemp[1],
                           'price':asostemp[2]})


# In[158]:

topshopdf = pandas.DataFrame({'time' :topshoptemp[0], 
                           'Name':topshoptemp[1],
                           'price':topshoptemp[2]})


# In[159]:

zaradf = pandas.DataFrame({'time' :zaratemp[0], 
                           'Name':zaratemp[1],
                           'price':zaratemp[2]})


# In[160]:

con = sqlite3.connect("ScraptedData.db")
c = con.cursor()


# In[145]:

query = ''' create table asos(
            Name char unique,
            Price char,
            Time char)
            '''
c.execute(query)
con.commit()


# In[106]:

query = ''' 
            create table topshop(
            name char unique,
            price float,
            time char)
            '''
c.execute(query)
con.commit()


# In[107]:

query = ''' 
            create table zara(
            name char unique,
            price float,
            time char)
            '''
c.execute(query)
con.commit()


# In[161]:

query=''' insert or ignore into asos values (?,?,?) '''
c.executemany(query, asosdf.to_records(index = False))
con.commit()


# In[162]:

query=''' insert or ignore into topshop values (?,?,?) '''
c.executemany(query, topshopdf.to_records(index = False))
con.commit()


# In[163]:

query=''' insert or ignore into zara values (?,?,?) '''
c.executemany(query, zaradf.to_records(index = False))
con.commit()


# In[164]:

#find the number of product in each table
for shops in newinurl.keys():
    query = '''select count(*) from '''+shops
    c.execute(query)
    con.commit()
    print shops,c.fetchone()


# In[130]:

print newinurl.keys()

