from fastapi import FastAPI



app = FastAPI()


@app.get("/health/", status_code=200)
async def hilling():
    return 'I am alive'

@app.get("/")
async def read_root():
    return {"Hello": "World"}

