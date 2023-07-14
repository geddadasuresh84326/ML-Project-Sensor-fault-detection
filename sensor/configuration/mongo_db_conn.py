import pymongo
from sensor.constant.database import DATABASE_NAME
import certifi
ca = certifi.where()

class mongoDBclient:
    client = None
    
    def __init__(self,database_name = DATABASE_NAME)->None:
        try:
            if mongoDBclient.client is None:
                mongo_db_url = "mongodb+srv://mongo1:<password>@cluster0.rmfujwk.mongodb.net/"
                mongoDBclient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile = ca)
                self.client = mongoDBclient.client
                self.database = self.client[database_name]
                self.database_name = database_name
        except Exception as e:
            raise e
        
