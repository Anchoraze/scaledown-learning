from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ScaleDown Learning Backend Running"}
