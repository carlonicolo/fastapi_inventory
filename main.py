from fastapi import FastAPI
from redis_om import get_redis_connection
import config

app = FastAPI()

# Connect to redis
redis = get_redis_connection(
    host=config.host,
    port=config.port,
    password=config.password
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
