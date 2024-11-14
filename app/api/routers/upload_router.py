import os
from uuid import uuid4, UUID
from base64 import b64decode
from typing import List, Optional
from mimetypes import guess_extension

from fastapi import APIRouter, Depends, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, func

from app.db.session import get_db
from app.models.models import images, pulse
from app.api.role_checker import RoleChecker
from app.schemas.upload_schemas import UploadNewFile


router = APIRouter()
upload_files_dir = os.path.join('uploaded_files')


def get_file_path(unique_id_full):
    file_path = os.path.join(upload_files_dir, str(unique_id_full))
    return file_path


def check_image_id(image_uuid, session):
    pulse_exists = session.query(images).filter(images.c.image_id == image_uuid).first()
    if not pulse_exists:
        return True
    return False


def check_pulse_id(pulse_id, session):
    pulse_exists = session.query(pulse).filter(pulse.c.id == pulse_id).first()
    if not pulse_exists:
        return True
    return False


@router.get("/image/{image_uuid}")
async def get_images(image_uuid: UUID, session: Session = Depends(get_db)):
    if check_image_id(image_uuid, session):
        raise HTTPException(status_code=404, detail="There is no image with this id")
    try:
        path = session.query(images.c.full_name).filter(images.c.image_id == image_uuid).first()
        path_res = get_file_path(path[0])
        return FileResponse(path_res)
    except Exception:
        raise HTTPException(status_code=500, detail="Send file error")


@router.post("/pulse/{id}/image")
async def upload_image(request: Request, id: int, files: List[UploadFile] = File(...), session: Session = Depends(get_db), role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    if check_pulse_id(id, session):
        raise HTTPException(status_code=404, detail="There is no pulse with this id")

    # checking images count
    images_count = session.query(func.count()).select_from(images).where(images.c.pulse_id == id).scalar()
    if images_count + len(files) >= 101:
        raise HTTPException(status_code=403, detail="you can't upload more than 100 images")

    # uuid generation, second part for files extensions
    for file in files:
        unique_id = f"{uuid4()}"
        unique_id_full = f"{unique_id}{os.path.splitext(file.filename)[1]}"

        os.makedirs(upload_files_dir, exist_ok=True)
        image_path = get_file_path(unique_id_full)

        with open(image_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        val = insert(images).values({"image_id": unique_id, "pulse_id": id, "full_name": unique_id_full, "image_path": f"https://vmesteapp.ru/content/image/{unique_id}"})
        session.execute(val)
        session.commit()
    raise HTTPException(status_code=200, detail="OK")


@router.delete("/image/{delete_image_uuid}")
def delete_image(request: Request, delete_image_uuid: UUID, session: Session = Depends(get_db),
                 role_checker=RoleChecker(allowed_roles=["user"])):
    role_checker(request)
    image_full_name = session.query(images.c.full_name).where(images.c.image_id == delete_image_uuid).first()
    image_path = get_file_path(image_full_name.full_name)
    try:
        os.remove(image_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Error when deleting an image")
    session.execute(delete(images).where(images.c.image_id == delete_image_uuid))
    session.commit()
