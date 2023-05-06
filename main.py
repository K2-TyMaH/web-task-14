import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_limiter import FastAPILimiter

from src.conf.config import settings
from src.routes import contacts, auth, users

app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are used by the app, such as databases or caches.

    :return: A list of coroutines
    :doc-author: Trelent
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


origins = [
    "http://localhost:3000", 'http://127.0.0.1:5500', 'http://localhost:5500',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.get("/")
def read_root():
    """
    The read_root function is a view function that returns a dictionary
    representing the root of the Contacts API. The dictionary contains one key,
    &quot;message&quot;, which has as its value &quot;Contacts API&quot;. This message will be returned to
    the client in JSON format.

    :return: A dictionary with a key &quot;message&quot; and value &quot;contacts api&quot;
    :doc-author: Trelent
    """
    return {"message": "Contacts API"}
