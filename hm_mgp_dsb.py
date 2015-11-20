import sqlite3
import urllib
from bs4 import BeautifulSoup
import time
import re
import os
import urllib2
from urllib import FancyURLopener
from random import choice

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

class MyOpener(FancyURLopener, object):
    version = choice(user_agents)

myopener = MyOpener()

os.getcwd()
os.chdir("c:/Users/Desktop/pricing/")

#create data base
conn = sqlite3.connect("price_data_dsb_HM_mgp.db")
c = conn.cursor()
#create table
c.execute("""create table Price_data_2015_11_20_01(
name text,
price text,
cat text,
shop text)""");
conn.commit()
query = """insert or ignore into Price_data_2015_11_20_01 values(?,?,?,?)"""



#dsb get product catgory list
dsb_dress = myopener.open("http://www.dressabelle.com.sg/").read()
soup_dsb = BeautifulSoup(dsb_dress,"html.parser")
dsb_category_list = {}
for category in soup_dsb.find_all("li", class_="inactive parent deeper")[1].find_all("li"):
    dsb_category_list[category.find("a").getText()] ="http://www.dressabelle.com.sg"+category.find("a")["href"]


#mgp get product catgory list
mgp_html = myopener.open("https://mgplabel.com/").read()
soup_mgp = BeautifulSoup(mgp_html,"html.parser")
mgp_category_list = {}
for category in soup_mgp.find("ul",class_="sf-menu").find_all("li")[2].find_all("li"):
    mgp_category_list[category.find("a").getText()] =category.find("a")["href"]


#h&m get product category list
hm_dress = myopener.open("http://www.hm.com/sg/subdepartment/LADIES").read()
soup_hm = BeautifulSoup(hm_dress,"html.parser")
hm_category_list = {}
for category in soup_hm.find("ul",class_="products single").find_all("a"):
    hm_category_list[category.getText()] = category["href"]


if __name__ == "__main__":
    #SCRAPE h&m
    print "----------------"
    print "scraping h&m.com"
    for cat in hm_category_list.keys():
        HM_scraper(cat)
    #dsb scrape
    print "----------------"
    print "scraping dressabelle.com"
    for cat in dsb_category_list:
        dsb_scraper(cat)
    #mgblabel    
    print "----------------"
    print "scraping mgpleble.com"
    for category in mgp_category_list.keys():
        counter = 0
        mgb_dress = myopener.open(mgp_category_list[category]+"?n=10000").read()
        soup_mgb = BeautifulSoup(mgb_dress,"html.parser")
        for item in soup_mgb.find("ul",id="product_list").find_all("div",class_="right_block"):
            c.execute(query,(item.find("a").getText(),item.find("span",class_="price").getText(),category,"mgblabel"))
            counter += 1
        print str(counter) +" "+category+" from mgblabel are downloaded"
    conn.commit()
    print "data collection done!"
    conn.close()


def HM_scraper(category):
    print "------------"
    print "current category:" + category
    current_page = 1
    end_page =False
    counter = 0
    while not end_page:
        if current_page == 1:
            hm_dress = myopener.open(hm_category_list[category]).read()
            soup_hm = BeautifulSoup(hm_dress,"html.parser")
        print "current page:" + str(current_page)
        for item in soup_hm.find_all("span",class_="product-info"):
            c.execute(query,(item.find("span",class_="details").getText().strip(),item.find("span",class_="price").getText().strip() ,category,"H&M"))
            counter +=1
            conn.commit()
            #print item.find("span",class_="details").getText().strip()
            #print item.find("span",class_="price").getText().strip()  
        try:
            hm_dress = myopener.open("http://www.hm.com/sg/subdepartment/LADIES"+soup_hm.find("li",class_="next").find('a')['href']).read()
            #print "http://www.hm.com/sg/subdepartment/LADIES"+soup_hm.find("li",class_="next").find('a')['href']
            soup_hm = BeautifulSoup(hm_dress,"html.parser")
            current_page += 1
        except:
            end_page = True
    print str(counter) +" "+category+" from H&M are downloaded"
 

def dsb_scraper(category):
    print "------------"
    print "current category:" + category
    current_page = 1
    end_page =False
    counter = 0
    while not end_page:
        if current_page == 1:
            page_html = myopener.open(dsb_category_list[category]).read()
            soup_dsb = BeautifulSoup(page_html,"html.parser")
        print "current page:" + str(current_page)
        for divs in soup_dsb.find_all("div",class_="quick-view-cont hidden-phone hidden-tablet"):
            c.execute(query,(divs.find("div",class_="title-container").find("h3").find("a").getText(),divs.find("div",class_="PricesalesPrice").find("span", class_="PricesalesPrice").getText(),category,"dsb"))
            counter += 1
            conn.commit()
            #print divs.find("div",class_="title-container").find("h3").find("a").getText()
        try:
            page_html = myopener.open("http://www.dressabelle.com.sg"+soup_dsb.find("a",class_="pagenav next")['href']).read()
            #print "http://www.dressabelle.com.sg"+soup_dsb.find("a",class_="pagenav next")['href']
            soup_dsb = BeautifulSoup(page_html,"html.parser")
            current_page += 1
        except:
            end_page = True
    print str(counter) +" "+category+" from dressabelle are downloaded"
