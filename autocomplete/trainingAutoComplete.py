from autocomplete import models
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db=client.articles

def getAllEntities():
    
    try:
        return list(db.articles.find( { },{"entities.entity":1}))
    except Exception as e: 
        print(e)


entityList = getAllEntities()



def getAllEntitiesAsString():
    string = ""

    for article in entityList:
        for entity in article['entities']:
            string +=entity['entity']+" "
            
    return string




trainingString = getAllEntitiesAsString()



try:
    models.train_models(trainingString)
    print("Training Completed")
except Exception as e:
    print(e)
