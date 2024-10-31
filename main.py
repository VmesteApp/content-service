import os
from fastapi import FastAPI
from app.api.routers import tag_router, pulse_router, application_router, upload_router, feed_router, complaints_router
from app.api.jwt_decoder import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(root_path="/content")

app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
    )


app.include_router(application_router.router)
app.include_router(pulse_router.router)
app.include_router(tag_router.router)
app.include_router(upload_router.router)
app.include_router(feed_router.router)
app.include_router(complaints_router.router)
app.debug = os.environ.get("DEBUG")
