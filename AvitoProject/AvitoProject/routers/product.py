from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND
from database import crud
from database.database import get_db
from services import product_service, image_service
from database.shemas import ProductRequest
from routers.user import get_current_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def get_all_products(request: Request, searchCategory: str = '', searchWord: str = '',
                           db: Session = Depends(get_db)):
    filtered_products = product_service.get_all_products(db, searchCategory, searchWord)

    categories = crud.get_all_categories(db)
    categories_dto = []
    for category in categories:
        categories_dto.append(category.name)
    context = {"request": request, "products": filtered_products, "categories": categories_dto}
    return templates.TemplateResponse("products.html", context)


@router.get("/product/{id}", response_class=HTMLResponse)
async def get_product_by_id(request: Request, id: int, db: Session = Depends(get_db)):
    product_db = crud.get_product_by_id(db, id)

    images = image_service.get_images_of_product_description(db, id)

    context = {
        "request": request,
        "product": product_db,
        "images": images
    }
    return templates.TemplateResponse("product-info.html", context)


@router.post("/product/delete/{product_id}")
async def delete_product(request: Request,
                         product_id: int,
                         db: Session = Depends(get_db)
                         ):
    user_id = await get_current_user(request)
    if user_id is None:
        return RedirectResponse(url="/login")
    crud.delete_product(db, product_id)
    return RedirectResponse(url=f'/profile/', status_code=HTTP_302_FOUND)


@router.get('/my/products', response_class=HTMLResponse)
async def get_user_products(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    products = product_service.get_products_from_user(db, user)
    context = {"request": request, "products": products, "user": user}
    return templates.TemplateResponse("users-products.html", context)


@router.post("/product/create", response_class=RedirectResponse)
async def create_product(request: Request, file1: UploadFile = File(...), file2: UploadFile = File(...),
                         file3: UploadFile = File(...), db: Session = Depends(get_db)):
    user_id = await get_current_user(request)
    if user_id is None:
        return RedirectResponse(url="/login")
    form = await request.form()
    product_request: ProductRequest = ProductRequest(
        user_id=user_id,
        title=form['title'],
        description=form['description'],
        contact_phone=form['contact_phone'],
        contact_email=form['contact_email'],
        country=form['country'],
        city=form['city'],
        street=form['street'],
        price=form['price']
    )
    category = form['category']
    images = (await file1.read(), await file2.read(), await file3.read())
    product_service.save_product_with_image(db, product_request, images, category)
    return RedirectResponse(url="/my/products", status_code=303)
