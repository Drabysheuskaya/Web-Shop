from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from database.database import get_db
from routers.user import get_current_user
from services import complain_service

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get('/users/complain/{product_id}')
async def complain(request: Request, product_id: int):
    user_id = await get_current_user(request)
    if user_id is None:
        return RedirectResponse(url="/login")
    product_id: int = product_id
    context = {"request": request, "product_id": product_id}
    return templates.TemplateResponse('complain.html', context)


@router.post('/users/complain/{product_id}')
async def complain(request: Request, product_id: int, db: Session = Depends(get_db)):
    user_id = await get_current_user(request)
    if user_id is None:
        return RedirectResponse(url="/login")
    form = await request.form()
    complaint_description = form.get("complaint-description")
    msg = complain_service.save_problem_report(db, complaint_description, product_id, user_id)
    context = {"request": request, "product_id": product_id, "msg": msg}
    return templates.TemplateResponse('complain.html', context)