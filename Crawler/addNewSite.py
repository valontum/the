
# coding: utf-8

# In[28]:


from bs4 import BeautifulSoup
import urllib.request
import json
import re
import nltk
import csv
import pandas as pd
import concurrent.futures
import urllib.request

from pymongo import MongoClient
from datetime import datetime
# pprint library is used to make the output look more pretty


client = MongoClient("mongodb://localhost:27017")
db=client.articles
# Issue the serverStatus command and print the results


# In[9]:


articleUrls = [] #stores article urls
articleUrlsToCrawl = [] #stores article urls
articles = [] #stores articles
sources = [] #stores site patterns and other infos



def saveUrl(obj):
    
     
     db.urls.insert_one(obj)
        
        





def getArticlesUrl(file, source, rootUrl):
    import re
   
    
    soup = BeautifulSoup(file, "lxml")
        
  
    exec('items = ' + source["urlPattern"],locals())
     
    
    
    for item in locals()["items"]:
        try:
            
            if item["href"].find(source["rootUrl"])==-1:
                saveUrl({"articleUrl":source["rootUrl"]+item["href"], "rootUrl":source["rootUrl"], "rootUrl":rootUrl,"stored":0})

            else:
                saveUrl({"articleUrl":item["href"], "rootUrl":source["rootUrl"], "rootUrl":rootUrl, "stored":0})
        except Exception as e: 
            
            print(e)


def crawlPageTypeOpinionsUrlList(source):
    
    
    
    
    
    for i in range(0, source["size"]+1):      

        try:
            path = source["url"]+str(i)

            r = urllib.request.urlopen(path).read()

            getArticlesUrl(r, source, source["rootUrl"])    

            print ("Downloaded file: "+str(i) + " of "+str(source["size"]))

        except Exception as e: 
            
            print(e)
    
    






def insertSiteIntoDB(obj):

    source = obj
    try:
        if db.sites.find({"rootUrl":obj["rootUrl"]}).count() == 0:
            db.sites.insert_one(obj)
            print("Site successfuly stored!")
            crawlPageTypeOpinionsUrlList(source)
        
        else:
            print("Site already exists")
        
    except ValueError:
        print("Oops!  Something worng, Please try it once more")

    









def readNewSiteFromConsole():
    
    authorPattern = input("authorPattern: ") 
    bodyPattern = input("bodyPattern: ")
    category = input("category: ")
    datePattern = input("datePattern: ")
    rootUrl = input("rootUrl: ")
    size = int(input("size: "))
    titlePattern = input("titlePattern: ")
    url = input("url: ")
    urlPattern = input("urlPattern: ")
    
    source = {"authorPattern":authorPattern,"bodyPattern":bodyPattern,"category":category,"datePattern":datePattern,"rootUrl":rootUrl,"size":size,"titlePattern":titlePattern,"url":url,"urlPattern":urlPattern}
    
    
    insertSiteIntoDB(source)
  



def testQueries():
    
    url = input("url: ")
    print("Press 'x' for new url")
    while(True):
        
        query = input("query: ")
        if(query=="x" or query == "X"):
            url = input("url: ")
        
        else:
        
            try:
                r = urllib.request.urlopen(url).read()



                import re


                soup = BeautifulSoup(r, "lxml")


                exec('items = ' + query,locals())

                print(locals()["items"])

            except Exception as e: 
            
                print(e)
    
                 

            
                    

   

command = input("'t' for test, 'r' for new site entry")

if(command == 't'):
    testQueries()
else:
    readNewSiteFromConsole()



