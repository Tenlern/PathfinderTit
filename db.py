from pymongo import MongoClient
# from models import Flight
from pathfinder import Graph
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


# Функция для заполнения графа данными из БД
# graph - заполняемый объект
# type - тип транспорта
def make_graph(graph: Graph, type: str):
    # Проверяем пути в базе подходящие нужному виду транспорта
    for path in paths.find():
        graph.connect(path['from'], path['to'], path['duration'])
    return graph


# Находим список соседних узлов по существующим ребрам в базе данных
# Возвращает словарь с сосед - расстояние
# node - имя узла
def get_neighbors(node: str):
    res = {}
    for path in paths.find({'from': node}):
        res.setdefault(path['to'], path['duration'])
    return res


# Находим расстояния до всех узлов для оценки оптимального пути по алгоритму A*
def get_heuristics(end: str, start: str = None):
    data = heuristics_data.find_one({'name': end})
    if start is not None:
        return data['heuristics'][start]
    else:
        return data['heuristics']




