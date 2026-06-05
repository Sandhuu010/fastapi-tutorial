from typing import Annotated
from fastapi import FastAPI, Depends, Header , HTTPException

app = FastAPI()


def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/itemsss/")
def get_items(p: dict = Depends(pagination)):
    return p


@app.get("/users/")
def get_users(p: dict = Depends(pagination)):
    return p


#Database Dependency
def get_db():
    db= "DB Connection"
    try:
        yield db
    finally:
        print("Closing DB")

@app.get("/itemss/")
def read_items(db=Depends(get_db)):
    return {"db": db}

#Classes as Dependencies

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 10):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return commons

class AuthService:
    def __init__(self, token: str):
        self.token = token
        self.user = self.verify_token()

    def verify_token(self):
        if self.token == "secret":
            return "Sandhu"
        return "Invalid"
    
@app.get("/profile/")
def profile(auth: AuthService = Depends()):
    return {"user": auth.user}

#Sub-Dependencies

def query_extractor(q: str | None = None):
    return q

def common_parameters(q: str = Depends(query_extractor), skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
def read_items(commons: dict = Depends(common_parameters)):
    return commons

#=============================================================

def get_token(token: str | None = None):
    return token

def get_current_user(token: str = Depends(get_token)):
    if token == "secret":
        return {"user": "Sandhu"}
    return {"user": "guest"}

@app.get("/profile/")
def profile(user: dict = Depends(get_current_user)):
    return user

#===================================================================

def get_db():
    return "DB_CONNECTION"


def get_current_user(db = Depends(get_db)):
    return {"user": "Sandhu", "db": db}


@app.get("/dashboard/")
def dashboard(user = Depends(get_current_user)):
    return user


#Dependency in Path operation decorators

def verify_token():
    print("Token verified")

@app.get("/items/", dependencies=[Depends(verify_token)])
def read_items():
    return {"message": "Hello"}

#Decorator dependency = "run only"
#Parameter dependency = "run + give result"

def auth():
    print("Checking auth.....")

@app.get("/admin", dependencies=[Depends(auth)])
def admin_panel():
    return {"msg": "Welcome Admin"}

#===================================================================================

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

#Global dependencies

#app = FastAPI(dependencies=[Depends(verify_token)])  define global dependency
