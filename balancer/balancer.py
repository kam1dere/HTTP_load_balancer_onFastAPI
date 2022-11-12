from fastapi import BackgroundTasks, FastAPI
from typing import Union
import httpx
import time


app = FastAPI()
"""
Адрес сервера зависит от директории в которой запускается проект.
(корневая папка)_web(название сервиса)_n(номер инстанса):порт
"""
servers = [
    'bwg_web_1:8000',
    'bwg_web_2:8000',
    'bwg_web_3:8000',
    'bwg_web_4:8000',
    'bwg_web_5:8000',
    'bwg_web_6:8000',
]


@app.get("/{path:path}")
async def balancer(background_check_server: BackgroundTasks, path: Union[str, None] = None):
    """
    Сам балансер. Берет первый сервер из очереди, а по завершении добавляет его в конец очереди.
    Реализован алгоритм Round Robin
    """
    try:
        host_name = servers.pop(0)
    except IndexError:
        return 'Все сломалось, расходимся'
    host_name = check_status_server(host_name, background_check_server)
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://{host_name}/{path}')
        servers.append(host_name)
    return response.content


def check_status_server(host_name, background_check_server):
    """
    Проверка работоспособности сервера, если жив > вернуть адресс,
    если нет, отправить его в фоновую задачу и взять следующий адрес из очереди
    """
    try:
        httpx.get(f'http://{host_name}/health/')
        return host_name
    except httpx.ConnectError:
        background_check_server.add_task(health_check_background, host_name)
        try:
            host_name = servers.pop(0)
            return check_status_server(host_name, background_check_server)
        except IndexError:
            return 'Все сломалось, расходимся'


def health_check_background(host_name):
    """
    Фоновая проверка мертвого сервера, каждые 5 секунд отправляет запрос,
    когда сервер ответит, он добавится в очередь
    """
    while True:
        time.sleep(5)
        try:
            httpx.get(f'http://{host_name}/health/')
            servers.append(host_name)
            break
        except httpx.ConnectError:
            continue
