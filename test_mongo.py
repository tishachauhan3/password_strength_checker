from pymongo import MongoClient

MONGO_URL = "mongodb+srv://tishahkdigiverse_db_user:yLuB8Ttt1aqh2rhF@cluster0.yacscfc.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URL)

db = client["password_checker"]
collection = db["weak_passwords"]

print("Connected to MongoDB!")

# insert test data

data = [
    {"type": "name", "value": "tisha"},
    {"type": "name", "value": "rahul"},
    {"type": "name", "value": "aman"},

    {"type": "birth_year", "value": "2004"},
    {"type": "birth_year", "value": "2002"},

    {"type": "keyword", "value": "admin"},
    {"type": "keyword", "value": "password"},
    {"type": "keyword", "value": "welcome"}
]

collection.insert_many(data)
print("Dataset inserted successfully!")

# check data
for item in collection.find():
    print(item)
