from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from database import crud
from database.database import get_db
from routers.user import get_current_user

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get('/profile', response_class=HTMLResponse)
async def profile(request: Request, db: Session = Depends(get_db)):
    user_id = await get_current_user(request)
    if user_id is None:
        return RedirectResponse(url="/login")
    user = crud.get_user_by_id(db, user_id)
    context = {"request": request, "user": user}
    return templates.TemplateResponse('profile.html', context)
