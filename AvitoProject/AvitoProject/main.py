from fastapi import FastAPI
from database.database import engine
from database import models
from routers import product, image, user, complain, profile, liked_products
from starlette.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(image.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(complain.router)
app.include_router(liked_products.router)
app.include_router(profile.router)
