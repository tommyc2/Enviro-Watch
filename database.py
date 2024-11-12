from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("DB")
client = MongoClient(uri)

db = client.get_database("EnviroWatch")
sensor_data_collection = db.get_collection("sensor_data_collection")

def find_database():
    if (db != None):
        print(f"""
              Found database: {db.name}\n
              Found collection: {sensor_data_collection}
              """)
        return db

def save_to_database(temp,hum,pressure,air):
    db.sensor_data_collection.insert_one(
        {
            "temp": temp,
            "humidity": hum,
            "pressure": pressure,
            "air_quality": str(air)
        }
    )

#find_database()



    





