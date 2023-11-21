import os
from pymongo import MongoClient
from pymongo import *  # Import the pymongo library
import json

MONGO_URI = "mongodb+srv://<username:password>@cluster0.al79tib.mongodb.net/"
DB_NAME = "SitesInfo"
COLLECTION_NAME = "Scan"

def insert_files_to_mongo(folder_path):
    # Connect to MongoDB Atlas
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Iterate through text files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            # Read content from the json file
            with open(file_path) as json_file:
                data = json.load(json_file)

            collection.insert_one(data)
            print(f"Inserted {filename} into MongoDB.")

    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    txt_files_directory = "sites_info"
    insert_files_to_mongo(txt_files_directory)
