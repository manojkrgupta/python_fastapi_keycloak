import uvicorn
from fastapi import FastAPI,Depends
from auth import authenticate
import logging

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
# logger.info("i am launching")
# logger.debug("am i in debug mode?")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/safe_house")
async def root(token = Depends(authenticate)):
    logger.info(token)
    return {"message": f"Hello {token['preferred_username']}!!"}

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8086)