from sensor.configuration.mongo_db_conn import mongoDBclient
from sensor.exception import SensorException
import sys,os
from sensor.logging import logging

def test_exception():
    try:
        100/0
    except Exception as e:
        raise SensorException(e,sys)
    

if __name__ == "__main__":
    # print("hello")
    mongo_client = mongoDBclient()
    print(mongo_client.client.test)
    print(mongo_client.database.list_collection_names())
    # try:
    #     logging.info("Executing test_exception function")
    #     test_exception()
    #     logging.info("test_exception function executed successfully")
    # except Exception as e:
    #     logging.info(e)
    #     print(e)