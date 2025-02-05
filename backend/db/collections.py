from pymongo import MongoClient
import os

MONGODB_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGODB_URI)
db = client['qlink']
user_collection = db.get_collection('user_profile')
call_logs_collection = db.get_collection('call_logs')
business_collection = db.get_collection('business')
entrepreneur_collection = db.get_collection('entrepreneur')
waitlist_collection = db.get_collection('waitlist')
