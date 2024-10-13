import os
from fastapi import FastAPI
from app.api.routers import tag_router, pulse_router, application_router
from app.api.jwt_decoder import AuthenticationMiddleware


app = FastAPI(openapi_prefix="/content")


app.add_middleware(AuthenticationMiddleware)
app.include_router(application_router.router)
app.include_router(pulse_router.router)
app.include_router(tag_router.router)
app.debug = os.environ.get("DEBUG")
