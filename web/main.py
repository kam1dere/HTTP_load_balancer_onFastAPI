from fastapi import FastAPI

app = FastAPI()


@app.get("/health/", status_code=200)
async def i_am_alive():
    """
    Для проверки работоспособности
    """
    return 'I am alive'


@app.get("/")
async def hello():
    """
    Страничка из тутора, для данной задачи её хватит
    """
    return {"Hello": "World"}
