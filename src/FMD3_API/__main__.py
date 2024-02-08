import uvicorn
from FMD3_API.app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# This comment should trigger the whole API to be updated to docker