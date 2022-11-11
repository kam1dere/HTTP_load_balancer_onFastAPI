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
async def balanc(background_tasks: BackgroundTasks, path: Union[str, None] = None):
    try:
        host_ID = servers.pop(0)
    except IndexError:
        return 'Все сломалось, расходимся'
    host_ID = proverka_life_server(host_ID, background_tasks)
    a = f'http://{host_ID}/{path}'
    print(a)
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://{host_ID}/{path}')
        servers.append(host_ID)
    return response.content


def proverka_life_server(host_ID, background_tasks):
    try:
        httpx.get(f'http://{host_ID}/health/')
        return host_ID
    except httpx.ConnectError:
        background_tasks.add_task(health_check, host_ID)
        try:
            host_ID = servers.pop(0)
            return proverka_life_server(host_ID, background_tasks)
        except IndexError:
            return 'Все сломалось, расходимся'


def health_check(host_ID):
    while True:
        time.sleep(3)
        try:
            httpx.get(f'http://{host_ID}/health/')
            servers.append(host_ID)
            break
        except httpx.ConnectError:
            continue
