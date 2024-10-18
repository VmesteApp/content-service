import os
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert

from app.models.models import images
# from app.schemas.images_schemas import UploadImage

router = APIRouter()


@router.post("/images/{pulse_id}")
async def upload_image(pulse_id: int, file: UploadFile = File(...), session: Session = Depends(get_db)):
    print(file)

    # uuid generation, second part for files extensions
    unique_id = f"{uuid4()}"
    unique_id_full = f"{unique_id}{os.path.splitext(file.filename)[1]}"

    image_path = os.path.join('app', 'upload_images')
    os.makedirs(image_path, exist_ok=True)
    print(image_path)
    file_path = os.path.join(image_path, unique_id_full)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    val = insert(images).values({"image_id": unique_id,
                  "pulse_id": pulse_id})
    session.execute(val)
    session.commit()
    return "OK"
