import os
from uuid import uuid4, UUID

from fastapi import APIRouter, Depends, File, UploadFile, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, func

from app.db.session import get_db
from app.models.models import images, pulse
from app.schemas.upload_schemas import DeleteImage


router = APIRouter()
upload_files_dir = os.path.join('uploaded_files')


def get_file_path(unique_id_full):
    file_path = os.path.join(upload_files_dir, unique_id_full)
    return file_path


def check_pulse_id(pulse_id, session):
    pulse_exists = session.query(pulse).filter(pulse.c.id == pulse_id).first()
    if not pulse_exists:
        return True
    return False


@router.get("/image/{pulse_id}")
async def get_images(request: Request, pulse_id: int, session: Session = Depends(get_db)):
    if request.state.role != "user":
        raise HTTPException(status_code=403, detail="Invalid role type")
    if check_pulse_id(pulse_id, session):
        raise HTTPException(status_code=404, detail="There is no pulse with this id")
    try:
        file_paths = session.query(images).where(images.c.pulse_id == pulse_id).all()
        return {"paths": [list(i) for i in file_paths]}
    except Exception:
        raise HTTPException(status_code=500, detail="Send file error")


@router.post("pulse/{id}/image")
async def upload_image(request: Request, pulse_id: int, file: UploadFile = File(...), session: Session = Depends(get_db)):
    if request.state.role == "user":
        if check_pulse_id(pulse_id, session):
            raise HTTPException(status_code=404, detail="There is no pulse with this id")

        # checking images count
        images_count = session.query(func.count()).select_from(images).where(images.c.pulse_id == pulse_id).scalar()
        if images_count >= 3:
            raise HTTPException(status_code=403, detail="you can't upload more than 3 images")

        # uuid generation, second part for files extensions
        unique_id = f"{uuid4()}"
        unique_id_full = f"{unique_id}{os.path.splitext(file.filename)[1]}"

        os.makedirs(upload_files_dir, exist_ok=True)
        image_path = get_file_path(unique_id_full)

        with open(image_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        val = insert(images).values({"image_id": unique_id, "pulse_id": pulse_id, "image_path": image_path})
        session.execute(val)
        session.commit()
        raise HTTPException(status_code=200, detail="OK")
    else:
        raise HTTPException(status_code=403, detail="Invalid role type")


@router.delete("/image/{uuid}")
def delete_image(request: Request, delete_image_uuid: UUID, session: Session = Depends(get_db)):
    if request.state.role == "user":
        session.execute(delete(images).where(images.c.image_id == delete_image_uuid))
        session.commit()
    else:
        raise HTTPException(status_code=403, detail="Invalid role type")
