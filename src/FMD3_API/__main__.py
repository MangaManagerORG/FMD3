import uvicorn

from FMD3.core.scheduler import start_scheduler_loop
from FMD3_API.app import app

if __name__ == "__main__":
    start_scheduler_loop()
    uvicorn.run(app, host="0.0.0.0", port=8000)
