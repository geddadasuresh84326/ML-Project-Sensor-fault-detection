import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
import os
from sensor.constant.env_variables import MONGODB_URL_KEY
ca = certifi.where()

class mongoDBclient:
    client = None
    
    def __init__(self,database_name = DATABASE_NAME)->None:
        try:
            if mongoDBclient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                mongoDBclient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile = ca)
                self.client = mongoDBclient.client
                # print("Mongo DB testing : ")
                # print(self.client.test)
                self.database = self.client[database_name]
                self.database_name = database_name
                # print(self.client.test)
        except Exception as e:
            raise e
        
