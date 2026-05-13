from fastapi import FastAPI

app = FastAPI(title="jmnav", version="0.1.0")


@app.get("/")
async def root():
    return {"message": "Hello from jmnav"}
