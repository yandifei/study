from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 使用 pydantic
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# @app.post("/items/")
# async def create_item(item: Item):
#     return item

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict