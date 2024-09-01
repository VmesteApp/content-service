from fastapi import FastAPI, HTTPException, Depends, Request,Form,status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import psycopg2
import fastapi_users

from sqlmodel import Session, select, delete

from app.models import Project, Profile, Application

from typing import Annotated

from app.db.session import get_session, init_db

from fastapi.security import OAuth2PasswordBearer
import jwt

from app.schemas.profile_schemas import Update_Profile
from app.schemas.project_schemas import Create_Project, UPDATE_PROJECT, DELETE_PROJECT
from app.schemas.applications_schemas import Send_Application, Verdict

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

import json

import sqlmodel

#from fastapi_users import fastapi_users

#from schemas.schemas import Create_project 


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#current_user = fastapi_users.current_user()

@app.on_event("startup")
async def startup_event():
    init_db()


def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

templates = Jinja2Templates(directory="templates")

#app.mount("/static", StaticFiles(directory="static"), name="static")

#current_user = fastapi_users.current_user()


@app.get("/profile/{user_id}")
async def get_user(user_id: int, session: Session = Depends(get_session)):
    project = select(Profile).where(Profile.user_id == user_id)
    res = session.exec(project)
    pr = res.one()
    print(pr)

@app.put("/profiles")
async def read_api(session: Session = Depends(get_session), up_profile: Update_Profile = Depends()):
    project = select(Profile).where(Profile.user_id == up_profile.user_id)
    res = session.exec(project)
    pr = res.one()
    pr.first_name = up_profile.first_name
    pr.middle_name = up_profile.middle_name
    pr.last_name = up_profile.last_name
    pr.date_birthday = up_profile.date_birthday
    pr.sex = up_profile.sex
    pr.city = up_profile.city
    pr.university = up_profile.university
    pr.bio = up_profile.bio
    session.add(pr)
    session.commit()
    session.refresh(pr)
    session.commit()
    

@app.post("/project")
async def create_project(session: Session = Depends(get_session), project: Create_Project = Depends()):
    project = Project(name = project.name, description=project.description, skills=project.skills)
    session.add(project)
    session.commit()
    

@app.put("/project")
async def read_api(session: Session = Depends(get_session), update_pr: UPDATE_PROJECT = Depends()):
    project = select(Project).where(Project.id == update_pr.id)
    res = session.exec(project)
    pr = res.one()
    pr.name = update_pr.name
    pr.description = update_pr.description
    pr.skills = update_pr.skills
    session.add(pr)
    session.commit()
    session.refresh(pr)
    session.commit()


@app.delete("/project")
async def read_api(session: Session = Depends(get_session), del_pr: DELETE_PROJECT = Depends()):
    stet = delete(Project).where(Project.id == del_pr.id)
    session.exec(stet)
    session.commit()

@app.post("/application")
async def read_api(session: Session = Depends(get_session), new_application: Send_Application = Depends()):
    application = Application(project_id = new_application.project_id, message = new_application.message, candidate_id=new_application.candidate_id, status="PENDING")
    session.add(application)
    session.commit()

    
@app.post("/application/verdict")
async def read_api(session: Session = Depends(get_session), verdict: Verdict = Depends()):
    appli = select(Application).where(Application.id == verdict.id)
    res = session.exec(appli)
    pr = res.one()
    pr.status = verdict.status
    session.add(pr)
    session.commit()
    session.refresh(pr)
    session.commit()

    

@app.get("/application/{project_id}")
async def read_api(project_id: int, session: Session = Depends(get_session)):
    appli = select(Application).where(Application.project_id == project_id)
    res = session.exec(appli)
    pr = res.all()
    print(pr)


