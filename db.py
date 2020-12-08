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


# Находим список соседних узлов по существующим ребрам в базе данных
# Возвращает словарь с сосед - расстояние
def get_neighbors(node: str):
    res = {}
    for path in paths.find({'from': node}):
        res.setdefault(path['to'], path['duration'])
    return res


# Находим расстояния до всех узлов для оценки оптимального пути по алгоритму A*
def get_heuristics(start: str, end: str):
    data = heuristics_data.find_one({'name': start})
    return data['heuristics'][end]




