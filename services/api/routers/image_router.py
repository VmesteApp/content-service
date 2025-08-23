import os
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from services.data.db_session.session import create_session
from services.api.role_checker import RoleChecker
from services.data.repositories.db_image_repository import DataBaseImageRepository

from src.domain.use_cases.image_use_case.upload_image import UploadImage
from src.domain.use_cases.image_use_case.get_image import GetImage
from src.domain.use_cases.image_use_case.delete_image import DeleteImage

from src.adapters.image_adapter import ImageAdapter

from src.domain.dto.image_dto.upload_image import UploadImageInputDto, UploadImageOutputDto
from src.domain.dto.image_dto.get_image import GetImageInputDto, GetImageOutputDto
from src.domain.dto.image_dto.delete_image import DeleteImageInputDto, DeleteImageOutputDto


router = APIRouter()
UPLOAD_FILES_DIR = os.path.join('uploaded_files')


@router.get("/image/{image_uuid}")
async def get_images(image_uuid: UUID, session: Session = Depends(create_session)):
    repository = DataBaseImageRepository(session, UPLOAD_FILES_DIR)

    input_dto: GetImageInputDto = ImageAdapter.request_to_get_image_input_dto(image_uuid)

    use_case = GetImage(repository)
    output_dto: GetImageOutputDto = use_case.execute(input_dto)

    if not output_dto.is_success:
        raise HTTPException(status_code=404, detail=output_dto.error_message)

    try:
        return FileResponse(output_dto.file_path)
    except Exception:
        raise HTTPException(status_code=500, detail="Send file error")


@router.post("/pulse/{pulse_id}/image")
async def upload_image(
    request: Request, 
    pulse_id: int, 
    files: List[UploadFile] = File(...),
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["user"])
):
    role_checker(request)

    repository = DataBaseImageRepository(session, UPLOAD_FILES_DIR)

    input_dto: UploadImageInputDto = await ImageAdapter.request_to_upload_image_input_dto(
        pulse_id=pulse_id,
        user_id=request.state.uid,
        files=files
    )

    use_case = UploadImage(repository)
    output_dto: UploadImageOutputDto = use_case.execute(input_dto)

    if not output_dto.is_success:
        raise HTTPException(status_code=400, detail=output_dto.error_message)

    return {"status": "OK", "message": "Images uploaded successfully"}


@router.delete("/image/{image_uuid}")
def delete_image(
    request: Request, 
    image_uuid: UUID, 
    session: Session = Depends(create_session),
    role_checker=RoleChecker(allowed_roles=["user"])
):
    role_checker(request)

    repository = DataBaseImageRepository(session, UPLOAD_FILES_DIR)

    input_dto: DeleteImageInputDto = ImageAdapter.request_to_delete_image_input_dto(
        image_uuid=image_uuid,
        user_id=request.state.uid
    )

    use_case = DeleteImage(repository)
    output_dto: DeleteImageOutputDto = use_case.execute(input_dto)

    if not output_dto.is_success:
        raise HTTPException(status_code=400, detail=output_dto.error_message)

    return {"status": "OK", "message": "Image deleted successfully"}
