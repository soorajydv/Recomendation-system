from pymongo import MongoClient

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/course')

# Check if the connection was successful
if client:
    print("MongoDB Connected")

# Access the 'course' database
db = client['course']

# Get a list of all collections in the 'course' database
collections = db.list_collection_names()

# Iterate through each collection and print its documents
for collection_name in collections:
    collection = db[collection_name]
    print(collection)
    

# Close the connection
client.close()
