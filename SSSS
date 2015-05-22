
# coding: utf-8

# In[1]:

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time
import pandas
from bs4 import BeautifulSoup
import urllib2


# In[2]:

asostemp=[[],[],[]];zaratemp=[[],[],[]];topshoptemp=[[],[],[]];f21temp=[[],[],[]]


# In[3]:

urls = {'asos':"http://www.asos.com/Women/New-In-Clothing/Cat/pgecategory.aspx?cid=2623",
        'zara':"http://www.zara.com/sg/",
        'f21':"http://www.forever21.com/Product/Category.aspx?br=f21&category=whatsnew_app&pagesize=30&page=1",
        'topshop':"http://sg.topshop.com/en/tssg/category/new-in-1087541"}


# In[4]:

driver = webdriver.Firefox()


# In[5]:

for shop in urls.keys():
    if shop == "topshop":
        driver.get(urls[shop])
        #wait = WebDriverWait(driver, 20)
        #wait.until(EC.element_to_be_clickable((By.ID,'sel_sort_field')))
        driver.find_element_by_xpath('//*[@id="sel_sort_field"]/option[contains(text(), "Newest")]').click()
        time.sleep(15)
        #wait.until(EC.element_to_be_clickable((By.ID,'sel_sort_field')))
        driver.find_element_by_xpath('//*[@title="Show page   200"]').click()
        time.sleep(20)
        
        for name in driver.find_elements_by_xpath("//li[@class='product_description']"):
            topshoptemp[1].append(name.text)
            topshoptemp[0].append(time.strftime("%d/%m/%Y"))
        for price in driver.find_elements_by_xpath("//li[@class='product_description']/following-sibling::li"):
            if ("Was" not in price.text) and (len(price.text)<=13):
                topshoptemp[2].append(price.text)
        
    elif shop == "asos":
        driver.get(urls[shop])
        wait = WebDriverWait(driver, 15)
        wait.until(EC.element_to_be_clickable((By.ID,'ctl00_ContentMainPage_ctlCategoryRefine_drpdwnPageSort')))
        driver.find_element_by_xpath('//*[@class="view-max-paged"]').click()
        wait.until(EC.element_to_be_clickable((By.ID,'ctl00_ContentMainPage_ctlCategoryRefine_drpdwnPageSort')))
        driver.find_element_by_xpath('//*[@id="ctl00_ContentMainPage_ctlCategoryRefine_drpdwnPageSort"]/option[contains(text(), "What\'s new")]').click()
        time.sleep(15)
        
        for name in driver.find_elements_by_class_name('desc'):
            asostemp[1].append(name.text)
            asostemp[0].append(time.strftime("%d/%m/%Y"))
        for price in driver.find_elements_by_xpath("//div[@class='productprice']/span[@class='price']"):
            asostemp[2].append(price.text)

    elif shop == "f21":
        driver.get(urls[shop])
        wait = WebDriverWait(driver, 20)
        wait.until(EC.element_to_be_clickable((By.ID,'ctl00_MainContent_ddlSortType')))
        driver.find_element_by_xpath('//*[@id="ctl00_MainContent_ddlSortType"]/option[contains(text(), "What\'s New")]').click()
        wait.until(EC.element_to_be_clickable((By.ID,'ctl00_MainContent_ddlSortType')))
        driver.find_elements_by_xpath('//li[@class="view_more"]//a[@class="PagerHyperlinkStyle" ]')[1].click()
        time.sleep(15)

        for name in driver.find_elements_by_xpath("//div[@class='DisplayName']"):
            if len(name.text) != 0:
                f21temp[1].append(name.text)
                f21temp[0].append(time.strftime("%d/%m/%Y"))
        for price in driver.find_elements_by_xpath("//font[@class='price']"):
                f21temp[2].append(price.text)
  
    elif shop =="zara":
        driver.get(urls[shop])
        wait = WebDriverWait(driver, 20)
        driver.find_elements_by_xpath('//ul[@id="mainNavigationMenu"]//li/a')[0].click()
        element = wait.until(EC.element_to_be_clickable((By.ID,'filter-btn')))
        
        for name in driver.find_elements_by_xpath("//a[@class='name item']"):
            zaratemp[1].append(name.text)
            zaratemp[0].append(time.strftime("%d/%m/%Y"))
        for price in driver.find_elements_by_xpath("//span[@class='price']/span"):
            zaratemp[2].append(price.text)

driver.close()


# In[6]:

print 'shop','\ttime','\tname','\tprice'
print 'asos\t',len(asostemp[0]), '\t',len(asostemp[1]), '\t',len(asostemp[2])
print 'topshop\t',len(topshoptemp[0]), '\t',len(topshoptemp[1]), '\t',len(topshoptemp[2])
print 'zara\t',len(zaratemp[0]), '\t',len(zaratemp[1]),'\t', len(zaratemp[2])
print 'f21\t',len(f21temp[0]), '\t',len(f21temp[1]),'\t', len(f21temp[2])


# In[7]:

asosdf = pandas.DataFrame({'time' :asostemp[0], 
                           'Name':asostemp[1],
                           'price':asostemp[2]})
topshopdf = pandas.DataFrame({'time' :topshoptemp[0], 
                           'Name':topshoptemp[1],
                           'price':topshoptemp[2]})
zaradf = pandas.DataFrame({'time' :zaratemp[0], 
                           'Name':zaratemp[1],
                           'price':zaratemp[2]})
f21df = pandas.DataFrame({'time' :f21temp[0], 
                           'Name':f21temp[1],
                           'price':f21temp[2]})


# In[8]:

con = sqlite3.connect("ScraptedData.db")
c = con.cursor()


# In[9]:

query=''' insert or ignore into asos values (?,?,?) '''
c.executemany(query, asosdf.to_records(index = False))
con.commit()
query=''' insert or ignore into topshop values (?,?,?) '''
c.executemany(query, topshopdf.to_records(index = False))
con.commit()
query=''' insert or ignore into zara values (?,?,?) '''
c.executemany(query, zaradf.to_records(index = False))
con.commit()
query=''' insert or ignore into f21 values (?,?,?) '''
c.executemany(query, f21df.to_records(index = False))
con.commit()


# In[11]:

#find the number of product in each table
for shops in urls.keys():
    query = '''select count(*) from '''+shops
    c.execute(query)
    con.commit()
    print shops,c.fetchone()


# In[10]:

#find the number of product in each table
for shops in urls.keys():
    query = '''select count(*) from '''+shops
    c.execute(query)
    con.commit()
    print shops,c.fetchone()


# In[ ]:
