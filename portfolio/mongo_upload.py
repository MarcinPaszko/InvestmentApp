from pymongo import MongoClient
import json
import os

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['admin']  # Change to your database name

# Path to the folder containing JSON files
folder_path = 'C:/Users/cryse/OneDrive/Pulpit/Investment-Portfolio/portfolio/stock_data'

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        print(f"Processing file: {filename}")
        # Load JSON file
        with open(os.path.join(folder_path, filename)) as f:
            data = json.load(f)
            print(data)  # Print the content of the JSON file

        # Ensure data is a non-empty dictionary
        if isinstance(data, dict) and data:
            # Extract collection name from filename
            collection_name = os.path.splitext(filename)[0]

            # Insert data into collection
            collection = db[collection_name]
            collection.insert_one(data)

            print(f"Uploaded data from {filename} to collection {collection_name}")
        else:
            print(f"No valid data found in {filename}")

print("All JSON files uploaded to MongoDB.")
