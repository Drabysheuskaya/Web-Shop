from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND
from starlette.templating import Jinja2Templates
from database.database import get_db
from routers.user import get_current_user
from services import product_service

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get('/users/likedProducts', response_class=HTMLResponse)
async def get_login(request: Request, db: Session = Depends(get_db)):
    user_id = await get_current_user(request)
    if user_id is None:
        return RedirectResponse(url="/login")
    print(user_id)
    products = product_service.get_liked_products_from_user(db, user_id)
    print(products)
    context = {"request": request, "products": products, "user": user_id}
    return templates.TemplateResponse("liked-products.html", context)


@router.post('/users/likedProducts')
async def add_to_liked_products(request: Request, db: Session = Depends(get_db)):
    user_id = await get_current_user(request)
    if user_id is None:
        return RedirectResponse(url="/login")
    form = await request.form()
    product_id: int = form.get("product_id")
    print("product_id:", product_id)
    product_service.add_to_liked_products(db, product_id, user_id)
    return RedirectResponse(url=f'/product/{product_id}', status_code=HTTP_302_FOUND)
