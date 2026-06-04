from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World-FastAPI Basics"}

@app.get("/about")
def about():
    return {"message":"This is About Page"}

@app.get("/contact")
def contact():
    return {"message":"Contact"}

@app.get("/student")
def student():
    return {
        "name":"Sandhuu",
        "Semester":5
    }

#Path Parameters

@app.get("/student/{student_id}/subject/{subject_id}")
def get_subject(student_id: int, subject_id: int):
    return {
        "student_id": student_id,
        "subject_id": subject_id
    }


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.get("/product/{product_id}")
async def product(product_id :int):
    return {
        "product_id": product_id
    }


#ENUM - create allowed values

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


class Category(str,Enum):
    electronics=  "electronics"
    clothing= "clothing"
    books= "books"

@app.get("/products/{category}")
async def get_product(category: Category):
    return {
        "category":category
    }


#Query Parameters

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {
        "item_id": item_id,
        "q": q
    }

@app.get("/productss/")
async def get_products(search: str = None):
    return {
        "search": search
    }

@app.get("/users/")
async def get_users(active: bool = False):
    return {
        "active": active
    }

@app.get("/students/")
async def get_students(
    semester: int = None,
    branch: str = None,
    limit: int = 10
):
    return {
        "semester": semester,
        "branch": branch,
        "limit": limit
    }

@app.get("/search/")
async def get_search(
    keyboard:str = None,
    page: int = 2
):
    return {
        "keyboard" : keyboard,
        "page" : page
    }


@app.get("/items/{item_id}")
async def read_item(
    item_id: str,
    q: str | None = None,
    short: bool = False
):
    item = {"item_id": item_id}

    if q:
        item.update({"q": q})

    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )

    return item

#Request Body using Pydantic's BaseModel

class Item(BaseModel):
    name: str
    price: float


@app.put("/itemss/{item_id}")
async def update_item(item_id: int, 
                      item: Item,
                      q: str | None = None
                      ):
    return {
        "item_id": item_id,
        "item": item,
        "q": q
    }

class Student(BaseModel):
    name: str
    semester: int
    branch: str
    cgpa: float

@app.post("/studentss")
async def create_student(student: Student):
    return student

#model_dump to convert pydantic model into python dict
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict