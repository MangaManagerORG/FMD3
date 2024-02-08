
from fastapi import FastAPI
from .routers import series, sources, chapters, settings
app = FastAPI()

app.include_router(series.router)#, prefix="/series", tags=["series"])
app.include_router(sources.router)
app.include_router(chapters.router)
app.include_router(settings.router)
