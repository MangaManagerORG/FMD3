
from fastapi import FastAPI

import FMD3.core
from .routers import series, settings,tasks, sources, chapters
from ..__version__ import __version__

app = FastAPI(on_shutdown=[FMD3.core.execute_termination_handler])

@app.get("/")
async def root():
    return {"message": "Successfully running FMD3 API",
            "version": __version__}
app.include_router(series.router)
app.include_router(settings.router)
app.include_router(tasks.router)
app.include_router(sources.router)
app.include_router(chapters.router)

from FMD3.core.scheduler import start_scheduler_loop
start_scheduler_loop()