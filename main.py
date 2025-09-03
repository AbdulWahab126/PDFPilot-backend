from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="First Fast API",
    description="Hello, this is my first fast api project",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to my first FastAPI project 🎉"}

@app.get("/hello/{name}")
def read_name(name):
    return{"message": f"Hello {name}, Welcome to my Fast API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
