from fastapi import FastAPI
from app.api.routers import tag_router, pulse_router, application_router


app = FastAPI()


app.include_router(application_router.router)
app.include_router(pulse_router.router)
app.include_router(tag_router.router)


