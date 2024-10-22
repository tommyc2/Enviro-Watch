from pymongo.mongo_client import MongoClient

password = "PW GOES HERE"
uri = f"mongodb+srv://tcmedion:{password}@mycluster.m9wolg3.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"

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





    





