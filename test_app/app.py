from fastapi import FastAPI
from pydantic import BaseModel
from test_app.ml import *
app = FastAPI()



class Item(BaseModel):
    comment: str


@app.get("/")
async def root():
    return {"Добавь /docs к адресу чтобы попасть на интерактивную доку где можно потестить апи": ":3"}

@app.post("/is_toxic")
def create_item(item: Item):
    return f'Cообщение : {item.comment} токсично на {voting([item.comment])[0]:.1%}'