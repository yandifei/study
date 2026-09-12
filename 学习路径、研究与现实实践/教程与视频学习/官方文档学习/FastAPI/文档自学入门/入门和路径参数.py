from enum import Enum

from fastapi import FastAPI



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 路径参数
@app.get("/items/{item_id}")
# async def read_item(item_id):
async def read_item(item_id: int):
    return {"item_id": item_id}


# 枚举路径
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    # 您可以使用以下方法获取实际值（str本例中为 a） ：model_name.value或者一般情况下，使用your_enum_member.value
    # "lenet"您也可以使用以下方式访问该值ModelName.lenet.value
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# 路径转换器
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

