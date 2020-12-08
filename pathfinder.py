from typing import Optional


# Класс для харнения данных графа на сервере
class Graph:

    # Инициализация
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    # В случае необходимости сделать граф без напрапления ребер
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist

    # Соедиение двух вершин ребром с указанным весом/дистанцией
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance

    # Метод нахождения соседих вершин или дистанции до конкретного соседа
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Метод для возвращения списка вершин
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name: str, parent):
        self.name = name
        self.parent = parent
        self.g = 0  # Distance to start node
        self.h = 0  # Distance to goal node
        self.f = 0  # Total cost

    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name

    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f

    # Print node
    def __repr__(self):
        return f'({self.name},{self.f})'


# Класс для работы с вершинами.
class Node:

    def __init__(self, name, parent):
        self.name: str = name
        self.parent: Optional[str] = parent
        self.f: int = 0
        self.g: int = 0
        self.h: int = 0

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.f < other.f


# Ленивый A*
def astar_search(graph, heuristics, start, end):
    # Создаем списки открытых и закрытых вершин
    open = []
    closed = []
    # Создаем вершины начала и конца маршрута
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Добавляем в открытый список стартовый узел
    open.append(start_node)
    # Проходимся по очереди в открытом списке
    print('Start searching')
    while len(open) > 0:
        print('Queue')
        # Сортируем список по самой низкой стоимости
        open.sort()
        # Забираем из очереди самый дешевый
        current_node = open.pop(0)
        # Добавляем пройденную вершину в список закрытых
        closed.append(current_node)

        # Проверка, пришел ли поиск к искомому узлу
        if current_node == goal_node:
            print('Found goal')
            path = []
            while current_node != start_node:
                # заполняем путь
                print('Searching return')
                path.append({"node": current_node.name, "duration": current_node.g})
                current_node = current_node.parent
            path.append({"node": start_node.name, "duration": start_node.g})
            # Возвращаем обратно путь
            return path[::-1]
        print('Found neighbors')
        # Ищем соседние узлы с рассматриваемым
        neighbors = graph.get(current_node.name)
        # Проверяем соседей
        for key, value in neighbors.items():
            # Создаем узел
            neighbor = Node(key, current_node)
            # Проверяем, не прошли ли мы данный узел
            if neighbor in closed:
                continue
            # Вычисляем стоимость пути
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # Проверяем нет ли соседнего узла в списке открытых с меньшей ценой
            if add_to_open(open, neighbor):
                print('New neighbor in queue')
                # Добавляем в очередь
                open.append(neighbor)
    # В случае отсутсвия пути возвращаем None
    return None


# Проверка соседнего узла
def add_to_open(open, neighbor):
    for node in open:
        if neighbor == node and neighbor.f > node.f:
            return False
    return True


# Оптимизированная версия А*
# Не использует локальный объект графа, а обращается к бд
def opt_astart(graph, heuristics, start, end):
    # Создаем списки открытых и закрытых вершин
    open = []
    closed = []
    # Создаем вершины начала и конца маршрута
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Добавляем в открытый список стартовый узел
    open.append(start_node)
    # Проходимся по очереди в открытом списке
    while len(open) > 0:
        print('Start searching')
        # Сортируем список по самой низкой стоимости
        open.sort()
        # Забираем из очереди самый дешевый
        current_node = open.pop(0)
        # Добавляем пройденную вершину в список закрытых
        closed.append(current_node)

        # Проверка, пришел ли поиск к искомому узлу
        if current_node == goal_node:
            print('Found goal')
            path = []
            while current_node != start_node:
                # заполняем путь
                print('Searching return')
                path.append({"node": current_node.name, "distance": current_node.g})
                current_node = current_node.parent
            path.append(start_node.name + ': ' + str(start_node.g))
            # Возвращаем обратно путь
            return path[::-1]
        print('Found neighbors')
        # Ищем соседние узлы с рассматриваемым
        neighbors = graph.get(current_node.name)
        print('Neighbors', current_node.name, neighbors.items())
        # Проверяем соседей
        for key, value in neighbors.items():
            print('Investigating neighbor')
            # Создаем узел
            neighbor = Node(key, current_node)
            # Проверяем, не прошли ли мы данный узел
            if neighbor in closed:
                continue
            # Вычисляем стоимость пути
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h
            # Проверяем нет ли соседнего узла в списке открытых с меньшей ценой
            if add_to_open(open, neighbor):
                print('New neighbor in queue')
                # Добавляем в очередь
                open.append(neighbor)
    # В случае отсутсвия пути возвращаем None
    return None
