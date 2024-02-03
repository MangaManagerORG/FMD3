from fastapi import FastAPI
from .routers import series

app = FastAPI()

app.include_router(series.router)#, prefix="/series", tags=["series"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
