
from fastapi import FastAPI
from .routers import series, settings,tasks#, sources, chapters
from ..__version__ import __version__

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Successfully running FMD3 API",
            "version": __version__}
app.include_router(series.router)
app.include_router(settings.router)
app.include_router(tasks.router)
# app.include_router(sources.router)
# app.include_router(chapters.router)
