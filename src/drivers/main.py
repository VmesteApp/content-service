from fastapi import FastAPI
from drivers.api.routers import profile


app = FastAPI()

app.include_router(profile.router)
# app.include_router(project.router)
# app.include_router(application.router)
# app.include_router(skills.router)
