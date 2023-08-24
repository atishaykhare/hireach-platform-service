import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from mongoengine import connect, disconnect
from redis import asyncio

from src.common.redis import redis_client
from src.common.config import settings
from src.common.utils import include_routers

app = FastAPI(debug=True)

# Disable OpenAPI documentation
# app.docs_url = None
# app.redoc_url = None

# Start up event
@app.on_event("startup")
async def startup():
    """
    """

    # create redis connection pool
    pool = asyncio.ConnectionPool.from_url(
        settings.REDIS_URL.unicode_string(), max_connections=10, decode_responses=False
    )

    # redis client connection
    app.state.redis_client = await asyncio.Redis(connection_pool=pool)

    # mongoengine DB connection
    connect(host=settings.DATABASE_URL.unicode_string())

# Start down event
@app.on_event("shutdown")
async def shutdown():
    """
    """

    # close redis client connection
    await app.state.redis_client.close()

    # close mongoengine DB connection
    disconnect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST"),
    allow_headers=settings.CORS_HEADERS,
)

# if settings.ENVIRONMENT.is_deployed:
#     sentry_sdk.init(
#         dsn=settings.SENTRY_DSN,
#         environment=settings.ENVIRONMENT,
#     )


# API for health check
@app.get("/healthz", status_code=200)
async def health_check():
    return {"status": "OK"}


# Include all routes
include_routers(app, "src/routers")
