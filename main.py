from typing import Optional

from fastapi import FastAPI, Body, Query
from fastapi.responses import JSONResponse
from models import Request, Response
from db import heuristics_data, paths, get_heuristics, get_neighbors, make_graph
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
@app.get('/schedule/lazy', response_model=Response)
async def get_schedule(
        request: Request = Body(...)
):
    graph = Graph()
    # Заполняем граф
    graph = make_graph(graph, request.type)
    print('Paths found')

    # Значения эвертической функции/дистанции
    heuristics = get_heuristics(request.arrival)
    print('Heuristics found')

    # Начинаем поиск оптимального пути
    path = astar_search(graph, heuristics, request.departure, request.arrival)

    # Если не найден маршрут, то возвращаем ошибку
    if path is None:
        return JSONResponse(status_code=404, content=dict(message="No path found", type=request.type))
    # Иначе формируем ответ
    response = Response(message="Path found", type=request.type)
    response.path = []
    # Заполняем маршрут
    for i in range(len(path)-1):
        path_data = paths.find_one(
            {
                "from": path[i]['node'],
                "to": path[i+1]['node'],
                "duration": path[i+1]['duration']-path[i]['duration']
            }
        )
        path_data.pop("_id")
        response.path.append(path_data)
    return response


# Тот же метод, что и выше, только с другим форматом вывода
@app.get('/schedule/lazy/plain')
async def get_schedule(
        request: Request = Body(...)
):
    graph = Graph()
    for path in paths.find():
        graph.connect(path['from'], path['to'], path['duration'])

    print('Paths found')

    heuristics = heuristics_data.find_one({'name': request.arrival})['heuristics']

    print('Heuristics found')

    path = astar_search(graph, heuristics, request.departure, request.arrival)

    if path is None:
        return JSONResponse(status_code=404, content=dict(message="No path found", type=request.type))

    response = []
    for i in range(len(path)-1):
        path_data = paths.find_one(
            {
                "from": path[i]['node'],
                "to": path[i+1]['node'],
                "duration": path[i+1]['duration']-path[i]['duration']
            }
        )
        path_data.pop("_id")
        response.append(path_data)
    return response


# Оптимизированный поиск при помощи Ant Colony TSP
@app.get('/schedule/ant')
async def get_schedule(
        start, end
):
    return None

@app.get('/heuristics')
async def get_heu(train_id: int = Query(None)):
    return get_neighbors('москва')


