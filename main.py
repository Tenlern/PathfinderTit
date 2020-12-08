from typing import Optional

from fastapi import FastAPI, Body, Query
from fastapi.responses import JSONResponse
from models import Request
from db import get_paths, heuristics_data, paths
from pathfinder import Graph, astar_search

app = FastAPI()


# Обработчик вызова api по индексу
@app.get('/')
async def root():
    return {'message': 'Hello World'}


# Обработчик вызова api по адресу domain/schedule по методу GET
# В качестве параметров принимает json из тела запроса
# Реализует ленивый поиск с болшими тратами памяти
# Для его работы нужны данные путей и отдельная подборка дальности между городами в базе данных
@app.get('/schedule/lazy')
async def get_schedule(
        # request: Request = Body(..., embed=True)
):
    graph = Graph()
    heuristics = {}

    for path in paths.find():
        graph.connect(path['from'], path['to'], path['duration'])

    print('Paths found')

    for cost in heuristics_data.find():
        heuristics.setdefault()

    print('Heuristics found')

    path = astar_search(graph, heuristics, 'талин', 'санкт-петербург')

    return path



# # Оптимимзированный A*
# @app.get('/schedule')
# async def get_schedule(
#         start, end
# ):
#     # Создаем списки открытых и закрытых вершин
#     open = []
#     closed = []
#     # Создаем вершины начала и конца маршрута
#     start_node = Node(start, None)
#     goal_node = Node(end, None)
#     # Добавляем в открытый список стартовый узел
#     open.append(start_node)
#
#     # Проходимся по очереди в открытом списке
#     while len(open) > 0:
#         # Сортируем список по самой низкой стоимости
#         open.sort()
#         # Забираем из очереди самый дешевый
#         current_node = open.pop(0)
#         # Добавляем пройденную вершину в список закрытых
#         closed.append(current_node)
#
#         # Проверка, пришел ли поиск к искомому узлу
#         if current_node == goal_node:
#             path = []
#             while current_node != start_node:
#                 # заполняем путь
#                 path.append(current_node.name + ': ' + str(current_node.g))
#                 current_node = current_node.parent
#                 path.append(start_node.name + ': ' + str(start_node.g))
#                 # Возвращаем обратно путь
#             return path[::-1]
#             # Ищем соседние узлы с рассматриваемым
#         neighbors = graph.get(current_node.name)
#         # Проверяем соседей
#         for key, value in neighbors.items():
#             # Создаем узел
#             neighbor = Node(key, current_node)
#             # Проверяем, не прошли ли мы данный узел
#             if (neighbor in closed):
#                     continue
#                 # Вычисляем стоимость пути
#                 neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
#                 neighbor.h = heuristics.get(neighbor.name, 0)
#                 neighbor.f = neighbor.g + neighbor.h
#                 # Check if neighbor is in open list and if it has a lower f value
#                 # Проверяем нет ли соседнего узла в списке открытых с меньшей ценой
#                 if add_to_open(open, neighbor):
#                     # Добавляем в очередь
#                     open.append(neighbor)
#         # В случае отсутсвия пути возвращаем None
#         return None


@app.get('/train/{train_id}')
async def get_train(train_id: int = Query(None)):
    if train_id is not None:
        return {'id': train_id, 'text': 'success'}
    else:
        return {'error': 'Code'}


@app.post('/train/{train_id}')
async def post_train(train_id: int = Query(None)):
    if train_id is not None:
        return {'id': train_id, 'text': 'success'}
    else:
        return {'error': 'Code'}

