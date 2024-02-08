import uvicorn
from FMD3_API.app import app
from __version__ import __version__


@app.get("/")
async def root():
    return {"message": "Successfully running FMD3 API",
            "version": __version__}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
