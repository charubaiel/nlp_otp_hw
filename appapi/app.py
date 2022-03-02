from fastapi import FastAPI
from pydantic import BaseModel
from appapi.ml import *
app = FastAPI()



class Item(BaseModel):
    comment: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/is_toxic")
def create_item(item: Item):
    return f'"{item.comment}" токсично на {voting([item.comment])[0]:.1%}'