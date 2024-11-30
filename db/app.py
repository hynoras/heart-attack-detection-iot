from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

client = MongoClient(config['ATLAS_URI'])
db = client[config['DB_NAME']]

