from datetime import datetime
from uuid import UUID
from typing import Annotated, Literal
from fastapi import FastAPI,Query,Path, Body, Cookie, Header,status
from enum import Enum
from pydantic import BaseModel, Field , HttpUrl, EmailStr
from fastapi.responses import RedirectResponse, FileResponse ,HTMLResponse , PlainTextResponse, Response

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

@app.get("/item/")
async def read_item(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit
    }

@app.get("/item/{item_id}")
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


@app.get("/item/{item_id}")
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


#Query Param and String Validation

@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(max_length=50)] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}

    if q:
        results.update({"q": q})

    return results

@app.get("/products/")
async def search_products(
    q: Annotated[
        str | None,
        Query(min_length=2, max_length=30)
                 ] = None
):
    return {"search": q}

#Path Param and Numeric Validations

@app.get("/students/{student_id}")
async def get_student(
    student_id: Annotated[
        int,
        Path(
            title="Student ID",
            ge=1,
            le=100
        )
    ]
):
    return {"student_id": student_id}

#Query Parameter Models

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

#Request Body Multiple Parameters

class Student(BaseModel):
    name: str
    semester: int


class Course(BaseModel):
    title: str


@app.put("/students/{student_id}")
async def update_student(
    student_id: int,
    student: Student,
    course: Course,
    active: bool = True,
):
    return {
        "student_id": student_id,
        "student": student,
        "course": course,
        "active": active,
    }

#Singular Values in body Body()

@app.post("/marks/")
async def add_marks(
    marks: Annotated[
        int,
        Body(ge=0, le=100)
    ]
):
    return {"marks": marks}

#Body Fields

class Item(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    return item

#Body- Nested Model

class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@app.post("/portfolio/")
async def create_portfolio(
    stocks: dict[str, float]
):
    return stocks

#Declare request Example Data

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Laptop",
                    "description": "Gaming Laptop",
                    "price": 50000,
                    "tax": 5000
                }
            ]
        }
    }


@app.post("/items/")
async def create_item(item: Item):
    return item

#Body Examples

from typing import Annotated
from fastapi import Body


@app.post("/items/")
async def create_item(
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Laptop",
                    "description": "Gaming Laptop",
                    "price": 50000,
                    "tax": 5000
                }
            ]
        )
    ]
):
    return item

#Extra Data Types

class User(BaseModel):
    id: UUID
    email: EmailStr
    website: HttpUrl
    created_at: datetime


@app.post("/users/")
async def create_user(user: User):
    return user

#Cookie Parameters

@app.get("/items/")
async def read_items(
    session_id: Annotated[str | None, Cookie()] = None
):
    return {"session_id": session_id}

@app.get("/profile/")
async def read_profile(
    session_id: Annotated[str | None, Cookie(title="Session Cookie",min_length=5)] = None,
    theme: Annotated[str | None, Cookie()] = None,
):
    return {
        "session_id": session_id,
        "theme": theme
    }

#Header Params

@app.get("/itemsss/")
async def read_items(
    user_agent: Annotated[str | None, Header()] = None
):
    return {"User-Agent" : user_agent}

#Cookie Parameter Models

class Cookies(BaseModel):
    session_id: str = Field(min_length=3)
    theme: str | None = None


@app.get("/items/")
async def read_items(
    cookies: Annotated[Cookies, Cookie()]
):
    return cookies

#Header Param Models

class CommonHeaders(BaseModel):
    host: str
    user_agent: str
    accept: str | None = None
    save_data : bool

@app.get("/items/")
async def read_items(
    headers: Annotated[
        CommonHeaders,
        Header()
    ]
):
    return headers

#Response Model - Return Type

class Student(BaseModel):
    name: str
    semester: int


@app.get("/student/")
async def get_student() -> Student:
    return {
        "name": "Sandhu",
        "semester": 5
    }

class StudentCreate(BaseModel):
    name: str
    email: str
    password: str


class StudentResponse(BaseModel):
    name: str
    email: str

@app.post(
    "/students/",
    response_model=StudentResponse
)
async def create_student(
    student: StudentCreate
):
    return student

class BaseUser(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseUser):
    password: str

@app.post("/register/")
async def register(user: UserCreate) -> BaseUser:
    return user

#Other return type annotations

@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse("/docs")

@app.get("/download")
async def download() -> FileResponse:
    return FileResponse("report.pdf")

@app.get("/")
async def home() -> HTMLResponse:
    return HTMLResponse(
        "<h1>Hello FastAPI</h1>"
    )

@app.get("/")
async def root() -> PlainTextResponse:
    return PlainTextResponse(
        "Hello World"
    )

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> dict | RedirectResponse:
    if teleport:
        return RedirectResponse(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )

    return {"message": "Here's your interdimensional portal."}

#Response Model Encoding Parameters

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]

#Extra Model

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

#Status Codes 

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

@app.post(
    "/userss/",
    status_code=status.HTTP_201_CREATED
)
async def create_user():
    return {"message": "User created"}