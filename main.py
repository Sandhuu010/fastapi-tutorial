from fastapi import FastAPI

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