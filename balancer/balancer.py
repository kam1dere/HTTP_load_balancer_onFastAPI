from fastapi import BackgroundTasks, FastAPI
from typing import Union
import httpx
import time


app = FastAPI()

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
    try:
        host_name = servers.pop(0)
    except IndexError:
        return 'Все сломалось, расходимся'
    host_name = check_life_server(host_name, background_check_server)
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://{host_name}/{path}')
        servers.append(host_name)
    return response.content


def check_life_server(host_name, background_check_server):
    try:
        httpx.get(f'http://{host_name}/health/')
        return host_name
    except httpx.ConnectError:
        background_check_server.add_task(health_check_background, host_name)
        try:
            host_name = servers.pop(0)
            return check_life_server(host_name, background_check_server)
        except IndexError:
            return 'Все сломалось, расходимся'


def health_check_background(host_name):
    while True:
        time.sleep(3)
        try:
            httpx.get(f'http://{host_name}/health/')
            servers.append(host_name)
            break
        except httpx.ConnectError:
            continue
