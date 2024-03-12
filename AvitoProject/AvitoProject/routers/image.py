from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response
from database import crud
from database.database import get_db

router = APIRouter(
    prefix='/images',
    tags=['image']
)

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/{image_id}", status_code=200)
async def get_image(image_id: int, db: Session = Depends(get_db)):
    image = crud.get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=image.image, media_type="image/jpeg")
