from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import config

app = FastAPI()

#Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000','http://127.0.0.1/8001'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Connect to redis
redis = get_redis_connection(
    host=config.host,
    port=config.port,
    password=config.password,
    decode_responses=config.decode_responses
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)


'''
@app.get("/")
async def root():
    return {"message": "Hello World"}
'''