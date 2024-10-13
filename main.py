import os
from fastapi import FastAPI
from app.api.routers import tag_router, pulse_router, application_router
from app.api.jwt_decoder import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(openapi_prefix="/content")


app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"]
)


app.include_router(application_router.router)
app.include_router(pulse_router.router)
app.include_router(tag_router.router)
app.debug = os.environ.get("DEBUG")
