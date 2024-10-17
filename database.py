# Source: https://github.com/tommyc2/IoT-Standards-And-Protocols-Project
# Author: Tommy Condon

from pymongo.mongo_client import MongoClient

password = "ENV VARIABLE HERE"
uri = f"mongodb+srv://tcmedion:{password}@mycluster.m9wolg3.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"

client = MongoClient(uri)

db = client.get_database("EnviroWatch")
collection = db.get_collection("sensordata").full_name

def find_database():
    if (db != None):
        print(f"""
              Found database: {db.name}\n
              Found {collection}
              """)
        return db

find_database()

#average_temp = db.collection.aggregate([
 #   {
 #       "$group": {
 #           "_id": None,
 #           "avgTemp": {"$avg": "$temp"}
 #       }
 #   }
#])

#for i in average_temp:
#    print(i["avgTemp"])






    





