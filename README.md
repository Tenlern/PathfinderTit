# PathfinderAPI
Web-api для поиска оптимального пути из пункта А в Б

Функции API:
0. /docs - Сгенерированная документация
1. /schedule - находит маршрут из А в Б по алгоритму А*
2. /schedule/lazy - неоптимизированная версия А* без использования вызовов БД

Для запуска сервера:
- uvicorn main:app --reload

Пример вызова API:

