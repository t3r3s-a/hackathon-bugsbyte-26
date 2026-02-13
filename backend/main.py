from fastapi import FastAPI
app = FastAPI()

@get("/")
def read_root():
    return {"message": "API FastAPI rodando"}
