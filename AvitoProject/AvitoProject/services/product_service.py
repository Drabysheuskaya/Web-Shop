from typing import Tuple
from sqlalchemy import or_, insert, select, text
from database import crud
from database.models import Product, Category, Image, liked_products
from sqlalchemy.orm import Session
from services import image_service
from database.shemas import ProductResponseShort, ProductRequest


def get_all_products(db: Session, category: str, searching_word: str):
    query = db.query(Product)

    if category and category.strip() != "":
        query = query.join(Product.categories).filter(Category.name == category)

    if searching_word and searching_word.strip() != "":
        search_pattern = f"%{searching_word}%"
        query = query.filter(
            or_(
                Product.title.like(search_pattern),
                Product.description.like(search_pattern)
            )
        )

    filtered_products = []
    for prod in query.all():
        product_response = ProductResponseShort(
            id=prod.id,
            title=prod.title,
            price=prod.price,
            country=prod.country,
            image=image_service.get_images_of_product(db, prod.id)[0]
        )
        filtered_products.append(product_response)

    return filtered_products


def get_product_by_id(db: Session, product_id: int):
    return crud.get_product_by_id(db, product_id)


def get_products_from_user(db: Session, user_id: int):
    products = db.query(Product).filter(Product.user_id == user_id).all()
    product_responses = []
    for prod in products:
        images = image_service.get_images_of_product_description(db, prod.id)
        preview_image = images[0] if images else None
        product_response = ProductResponseShort(
            id=prod.id,
            title=prod.title,
            price=prod.price,
            country=prod.country,
            image=preview_image.get("id")
        )
        product_responses.append(product_response)
    return product_responses


def get_liked_products_from_user(db: Session, user_id: int):
    query = text('''
            SELECT Product.*
            FROM Product
            JOIN LikedProduct ON Product.id = LikedProduct.product_id
            WHERE LikedProduct.user_id = :user_id
        ''')
    products = db.execute(query, {'user_id': user_id})
    filtered_products = []
    for prod in products:
        images = image_service.get_images_of_product_description(db, prod.id)
        preview_image = images[0] if images else None
        product_response = ProductResponseShort(
            id=prod.id,
            title=prod.title,
            price=prod.price,
            country=prod.country,
            image=preview_image.get("id")
        )
        filtered_products.append(product_response)
    return filtered_products


def save_product_with_image(db: Session, product_data: ProductRequest, images: Tuple, category_name: str):
    try:
        product = Product(
            user_id=product_data.user_id,
            title=product_data.title,
            description=product_data.description,
            contact_phone=product_data.contact_phone,
            contact_email=product_data.contact_email,
            country=product_data.country,
            city=product_data.city,
            street=product_data.street,
            price=product_data.price
        )
        category = db.query(Category).filter(Category.name == category_name).first()

        if not category:
            category = Category(name=category_name)
            db.add(category)

        product.categories.append(category)
        for data in images:
            if data is not None and len(data) > 0:
                image = Image(image=data)
                image.product = product
                product.images.append(image)
        db.add(product)
        db.commit()
    except Exception as e:
        raise e


def add_to_liked_products(db: Session, product_id: int, user_id: int):
    query = select(liked_products).where(
        (liked_products.c.product_id == product_id) & (liked_products.c.user_id == user_id)
    )
    existing_record = db.execute(query).fetchone()

    if existing_record:
        return
    values = {
        'product_id': product_id,
        'user_id': user_id
    }
    insert_stmt = insert(liked_products).values(values)
    db.execute(insert_stmt)
    db.commit()
