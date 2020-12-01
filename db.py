from pymongo import MongoClient
from models import Flight
from env import db

client = MongoClient(**db['db_connection'])
database = client[db['db_name']]


def get_flight(**params):
    collection = database['flights']
    res = collection.find_one(params)
    return res


def get_flights(**params):
    collection = database['flights']
    res = []
    for doc in collection.find(params):
        res.append(Flight(**doc))
    return res
