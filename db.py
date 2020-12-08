from pymongo import MongoClient
# from models import Flight
from env import db

client = MongoClient("mongodb+srv://reader:G2vAQBNr1Qn3EG1A@cluster0.z7vr7.mongodb.net/pathfinder_tit",
                     retryWrites=True, w="majority", tlsAllowInvalidCertificates=True)
database = client['pathfinder_tit']
paths = database['paths_test']
heuristics_data = database['heuristics']


def get_path(**params):
    collection = database['paths']
    res = collection.find_one(params)
    return res


def get_paths(params):
    res = []
    for doc in paths.find(params):
        res.append(doc)
    return res


def get_neighbors(node: str):
    res = {}
    for path in paths.find({
        'from': node
    }):
        res.setdefault(path['to'], path['duration'])




