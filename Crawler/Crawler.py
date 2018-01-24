
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
from pprint import pprint

client = MongoClient("mongodb://localhost:27017")
db=client.articles
# Issue the serverStatus command and print the results


# In[9]:


articleUrls = [] #stores article urls
articleUrlsToCrawl = [] #stores article urls
articles = [] #stores articles
sources = [] #stores site patterns and other infos




# In[11]:


  


# In[13]:


def readUrls():
    
    
    return pd.DataFrame(list(db.urls.find({"stored":0})))



   
    


# In[536]:









    



# In[17]:


def saveItemCSV(obj):
    try:
        db.items.insert(obj)
        db.urls.update_many({ "articleUrl": obj["url"] },{'$set': {"stored":1}},upsert=False)
    except Exception as exc:
	
        
        print("duplicated")

     
        
        
 
           






# In[ ]:



def crawlPageTypeOpinions():

   
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(crawlPageTypeOpinion, url, 60): url for url in range(0, len(articleUrlsToCrawl)-1)}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print("error")





def crawlPageTypeOpinion(i, timeout):
    import re
    items = []
    
    #for i in range(articleUrlsToCrawl.index.values[0], max):      
        
        
        
    try:
        path = articleUrlsToCrawl.loc[i]["articleUrl"];

        r = urllib.request.urlopen(path,timeout=timeout).read()

      
        soup = BeautifulSoup(r,"lxml")
            
        

            

            
            
            #print datetime

            
            
            
           
            
            

        exec('datetime = ' +sources.loc[sources["rootUrl"] == articleUrlsToCrawl.loc[0]["rootUrl"]]["datePattern"][0],locals())
            
            
            
            
            
            
            
            
            
            
            
            
          
            
            
            
        exec('title = '+sources.loc[sources["rootUrl"] == articleUrlsToCrawl.loc[0]["rootUrl"]]["titlePattern"][0],locals())
            
            #print title

        

            #print body
            
            
            
            
            
            

        exec('body = ' +sources.loc[sources["rootUrl"] == articleUrlsToCrawl.loc[0]["rootUrl"]]["bodyPattern"][0],locals())
            
            
           
        
            
        
        
    
            
            



            #print '.'.join(text)


    

            
            #print author


           
           
           
            
            

        exec('author = ' +sources.loc[sources["rootUrl"] == articleUrlsToCrawl.loc[0]["rootUrl"]]["authorPattern"][0],locals())
            
            
            
            
            
            
            
       
            
        saveItemCSV({"source" : sources.loc[sources["rootUrl"] == articleUrlsToCrawl.loc[0]["rootUrl"]]["rootUrl"][0], "title" : re.sub('[^a-zA-Z ]', '', locals()['title']), "body" : BeautifulSoup(locals()['body'],"lxml").text.replace("\n",""), "author" : locals()['author'], "datetime" : locals()['datetime'], "url" : path, "category":sources.loc[sources["rootUrl"] == articleUrlsToCrawl.loc[0]["rootUrl"]]["category"][0], "analysed":0 })
          
       
     
          
            
        print ("Downloaded file "+str(i+1)+" of "+str(len(articleUrlsToCrawl)))
            
    except Exception as e: 
            
        print(path)
    
	
        print(db.urls.update_many({ "articleUrl": path },{'$set': {"stored":"Not Accessible"}},upsert=False))
        print ("File not Downloaded "+str(i+1)+" of "+str(len(articleUrlsToCrawl)))
        
    
    
    
    return items













# In[9]:

latestArticle = ""
updatedCount = 0

def saveUrl(obj):
    
    
    
     db.urls.update_many({"noExist": True}, {"$setOnInsert": obj}, upsert = True)

        
        

def readSites():
    
    
    return pd.DataFrame(list(db.sites.find()))


def readLastArticle(rootUrl):
    
    obj = list(db.urls.find({"articleUrl":rootUrl}).limit(1))
    

    if len(obj) == 0:
        return True
    elif obj[0]["stored"]=="Not Accessible":
        return True
    else:
        return False



def getArticlesUrl(file, source, rootUrl):
    import re

    global updatedCount
    global latestArticle
    
    status = True
   
    
    soup = BeautifulSoup(file, "lxml")
        
  
    exec('items = '+source["urlPattern"],locals())
     
    
    
    for item in locals()["items"]:
        
        try:
            if item["href"].find(source["rootUrl"])==-1:
                if readLastArticle(source["rootUrl"]+item["href"]):
                    saveUrl({"articleUrl":source["rootUrl"]+item["href"], "rootUrl":source["rootUrl"], "rootUrl":rootUrl,"stored":0})
                    updatedCount = updatedCount+1
                else:
                    status = False
                    break
            else:

                if readLastArticle(item["href"]):
                    saveUrl({"articleUrl":item["href"], "rootUrl":source["rootUrl"], "rootUrl":rootUrl, "stored":0})
                    updatedCount = updatedCount+1
                else:
                    status = False
                    break
        except Exception as e: 
            
            print(e)

    return status

def crawlPageTypeOpinionsUrlList(source):   
    
    
    
    for i in range(0, 1000000000):      

        try:
            path = source["url"]+str(i)
            
            

            r = urllib.request.urlopen(path).read()

            status = getArticlesUrl(r, source, source["rootUrl"])    
            
            if status == False:
                break
                
                
            print ("Downloaded file: "+str(i) + " of "+str(source["size"]))

        except Exception as e: 
            
            print(e)
    
    













#load sources from site.csv
sources = readSites()



# In[537]:







for i in range(0,len(sources)):
    
    
    print("Downloaded Articles\n")
    updatedCount = 0
    
    
    crawlPageTypeOpinionsUrlList(sources.loc[i])
    print(sources.loc[i]["rootUrl"]+": "+str(updatedCount))












articleUrlsToCrawl =  readUrls()




crawlPageTypeOpinions()
