import pymongo
import pandas as pd
import json
import os
import certifi
ca = certifi.where()

# Provide the mongoclient url to connect python to mongodb
mongodb_client = pymongo.MongoClient("mongodb+srv://mongo1:mongo@cluster0.rmfujwk.mongodb.net/",tlsCAFile = ca)
test = mongodb_client.test 
db = "aps"
collection ="sensor"

# dataset link
dataset_link = "aps_failure_training_set1.csv"

if __name__ == "__main__":
    df = pd.read_csv(dataset_link)
    # print(test)
    # print(df.head())
    # print(db.list_collection_names())
    print(f"Rows and columns : {df.shape}")

    # converting data into json so that we can dump data into mongoDB
    df.reset_index(drop=True,inplace=True)

    json_df = list(json.loads(df.T.to_json()).values())
    # print(json_df[0])

    ## dumping into mongoDB
    df_len = df.shape[0]
    print(df_len)

    i = 33357
    while(i<df_len):
        mongodb_client[db][collection].insert_one(json_df[i])
        i +=1
        print(f"record : {i} dumping into MongoDB completed")
