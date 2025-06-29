import os
from fastapi import FastAPI
from services.api.routers import pulse_router
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
app.debug = os.environ.get("DEBUG")
