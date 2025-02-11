
import requests
import json
from datetime import date, timedelta
import time
import shutil
import os
from pymongo import MongoClient


API_KEY = 'XXX'


with open('assets_list.json', 'r') as json_file:
    assets = json.load(json_file)

# List of stock symbols
symbols = [asset['symbol'] for asset in assets]

# Get the date from the user
user_date = input("Provide recon data (DD-MM-YYYY): ")
user_date_obj = date(*map(int, reversed(user_date.split('-'))))

# Check if the date is a weekend
if user_date_obj.weekday() in [5, 6]:  # Saturday (5) or Sunday (6)
    print("This date is a weekend. No data can be derived.")
    exit()

# Create a dictionary to store stock data for each symbol
all_stock_data = {}

# Number of assets to download in each interval
assets_per_interval = 5

# Loop through intervals until a total of 50 assets are downloaded
for i in range(0, 50, assets_per_interval):
    # Fetch data for the current batch of assets
    current_symbols = symbols[i:i + assets_per_interval]
    for symbol in current_symbols:
        formatted_date = user_date_obj.strftime("%Y-%m-%d")
        endpoint = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{formatted_date}/{formatted_date}?adjusted=true&sort=asc&limit=120&apiKey={API_KEY}"
        response = requests.get(endpoint)

        if response.status_code == 200:
            data = response.json()
            # Assuming the structure of the response, adjust the keys accordingly
            stock_data = {
                "symbol": symbol,
                "name": next((asset['name'] for asset in assets if asset['symbol'] == symbol), ""),
                "closing_price": data.get("results", [])[0].get("c", None),
                "volume_weighted": data.get("results", [])[0].get("vw", None),
                "open_price": data.get("results", [])[0].get("o", None),
                "high_price": data.get("results", [])[0].get("h", None),
                "low_price": data.get("results", [])[0].get("l", None),
                "timestamp": data.get("results", [])[0].get("t", None),
                "num_trades": data.get("results", [])[0].get("n", None)
                # Add more fields as needed
            }
            all_stock_data[symbol] = stock_data
        else:
            print(f"No data available for {symbol} on {formatted_date}")

    # Wait for 60 seconds before the next interval, except for the last one
    if i + assets_per_interval < 50:
        print(f"Waiting for 60 seconds before the next interval for batch {i//assets_per_interval}...")
        time.sleep(60)

# Connect to MongoDB
#local:
#mongo_client = MongoClient('mongodb://localhost:27017')
mongo_client = MongoClient('mongodb://mongodb:27017')

db = mongo_client['admin']

# Generate the filename based on the user-provided date
filename = f'stock_data_polygon_{user_date_obj.year}_{user_date_obj.month:02d}_{user_date_obj.day:02d}.json'

# Save the data to the generated JSON file
with open(filename, 'w') as json_file:
    json.dump(all_stock_data, json_file, indent=2)

print(f"Stock data saved to {filename}")

# Insert the data into MongoDB
collection_name = f'stock_data_polygon_{user_date_obj.year}_{user_date_obj.month:02d}_{user_date_obj.day:02d}'
collection = db[collection_name]
collection.insert_one(all_stock_data)

print(f"Data inserted into MongoDB collection: {collection_name}")

print("Moving file to database...")
time.sleep(15)

# Move the file to the stock_data directory
#local
#destination_path = os.path.join(os.getcwd(), 'stock_data', filename)
destination_path = os.path.join('/app/stock_data', filename)
shutil.move(filename, destination_path)

print(f"File moved to {destination_path}")

# Close MongoDB connection
mongo_client.close()
