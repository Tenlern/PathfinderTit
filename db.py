from pymongo import MongoClient
import os
from pathfinder import Graph
from env import db

client = MongoClient(f"mongodb+srv://Heroku:mKU9xNohEpL62uVr@intertrans.tghpe.mongodb.net/schedule)",
                     retryWrites=True, w="majority", tlsAllowInvalidCertificates=True)
database = client['schedule']
paths = database['flights']
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




