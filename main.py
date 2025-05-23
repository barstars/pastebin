from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

from database import DataManager
from url import Url


app = FastAPI()

class DataText(BaseModel):
    text: str

class DataUser(DataText):
    ip_address: str
    useragent: str

@app.on_event("startup")
async def startup_event():
    app.state.db = DataManager()
    app.state.url_generator = Url(app.state.db)
    print("База данных готова")

@app.on_event("shutdown")
async def shutdown_event():
    print("Остановка приложения")



async def create(db: DataManager, url_generator: Url, data: DataUser):
    data_dict = data.model_dump()
    url = await url_generator.generateUrl()
    data_dict["url"] = url
    await db.add(**data_dict)
    return url

@app.post("/add-text")
async def add_text_post(request: Request, data: DataText):
    db = request.app.state.db
    url_generator = request.app.state.url_generator

    user_data = DataUser(
        text=data.text,
        ip_address=request.client.host,
        useragent=request.headers.get("user-agent")
    )
    url = await create(db, url_generator, user_data)
    return {"url": url}


@app.get("/add-text")
async def add_text_get():
    return FileResponse("add-text/index.html")

@app.get("/add-text/{file_name}")
def get_add_text_files(file_name: str):
    return FileResponse(f"add-text/{file_name}")

@app.get("/mytext")
async def my_text(request:Request):
    return await request.app.state.db.read_from_useragent(request.headers.get("user-agent"))


@app.get("/")
async def index(request: Request):
    return await request.app.state.db.read_all()


@app.get("/{api}")
async def get_text(api: str, request: Request):
    db = request.app.state.db
    result = await db.read_text(api)
    if result:
        return {"text": result}
    return JSONResponse(status_code=404, content={"message": "URL не существует"})