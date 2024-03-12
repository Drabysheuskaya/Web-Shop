from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from database.database import get_db
from database.models import User
from services import user_service
from database.shemas import UserRequest

router = APIRouter()

SECRET_KEY = 'EUGVUTERTG;UHR;GRUG;UHRGHKLFNBL;KERLITVJRUIHTNILUHRNBUHTGIEUHBRTGBDIUHBGIOGUIRTBHGOIDUBOGIUH'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='users/token')

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory="templates")


def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401)
    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401)
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_auth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            return None
        return user_id
    except JWTError:
        return None


@router.get("/register")
async def register_page(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("register.html", context)


@router.post("/registration")
async def register_user(request: Request, db: Session = Depends(get_db)):
    form = await request.form()

    user_request = UserRequest(
        first_name=form.get("name"),
        last_name=form.get("surname"),
        telephone_number=form.get("phoneNumber"),
        password=bcrypt_context.hash(form.get("password")),
        date_of_birth=form.get("dateOfBirthday"),
        email=form.get("email"),
    )
    msg = user_service.create_user(db, user_request)
    context = {"request": request, "successMessage": msg}
    return templates.TemplateResponse("register.html", context, status_code=201)


@router.get('/login', response_class=HTMLResponse)
def get_login(request: Request):
    context = {"request": request}
    return templates.TemplateResponse('login.html', context)


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_auth_form()
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

        await login_for_access_token(response=response, form_data=form, db=db)
        return response
    except HTTPException:
        msg = "Incorrect Username or Password"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.post("/token")
async def login_for_access_token(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed"
    token = create_access_token(user.email, user.id, timedelta(minutes=20))
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True
