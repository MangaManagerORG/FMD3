import multiprocessing

import uvicorn
from FMD3_API.app import app



if __name__ == "__main__":
    multiprocessing.freeze_support()
    uvicorn.run(app, host="0.0.0.0", port=8000)

