import os
from fastapi import FastAPI
from services.api.routers import pulse_router
# from services.api.routers import application_router
from services.api.routers import feed_router
# from services.api.routers import complaint_router
from services.api.routers import admin_router
from services.api.routers import image_router
# from services.api.routers import notification_router
from services.api.routers import tag_router

from services.api.jwt_decoder import AuthenticationMiddleware
from services.data.db_session.session import global_init
from fastapi.middleware.cors import CORSMiddleware


global_init()

app = FastAPI(root_path="/content")

app.add_middleware(AuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
    )

app.include_router(pulse_router.router)
# app.include_router(application_router.router)
app.include_router(admin_router.router)
app.include_router(feed_router.router)
# app.include_router(complaint_router.router)
# app.include_router(notification_router.router)
app.include_router(image_router.router)
app.include_router(tag_router.router)

app.debug = os.environ.get("DEBUG")
