from flask import Flask
from flask_pymongo import pymongo
from app import app
import os
CONNECTION_STRING = os.getenv("MONGO_CON")
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')