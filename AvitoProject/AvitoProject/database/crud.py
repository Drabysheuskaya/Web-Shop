from sqlalchemy.orm import Session
from database.models import Image, Category, ProblemReport, User, Product
from database.shemas import ImageResponse, ImageRequest, RoleRequest, RoleResponse, CategoryResponse, CategoryRequest, \
    ProblemReportRequest, UserRequest, UserResponse, ProductRequest, ProductResponse


def get_image_by_id(db: Session, image_id: int):
    image = db.query(Image).filter(Image.id == image_id).first()
    return ImageResponse(image=image.image, id=image.id)


def create_image(db: Session, image_request: ImageRequest):
    db_image = Image(**image_request.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def update_image(db: Session, image_id: int, image_request: ImageResponse):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image is None:
        raise Exception(f'No image with id {image_id}')
    db_image.image = image_request.image
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, image_id: int):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image is None:
        raise Exception()
    db.query(Image).filter(Image.id == image_id).delete()
    db.commit()



def get_category_by_id(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    return CategoryResponse(id=category.id, name=category.name)


def get_all_categories(db: Session):
    categories = db.query(Category).all()
    return categories


def create_category(db: Session, category_response: CategoryRequest):
    db_category = Category(**category_response.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category_request: CategoryRequest):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise Exception(f'No image with id {category_id}')
    db_category.name = category_request.name
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category is None:
        raise Exception()
    db.query(Category).filter(Category.id == category_id).delete()
    db.commit()


def get_problem_report_by_id(db: Session, problem_report_id: int):
    problem_report = db.query(ProblemReport).filter(ProblemReport.id == problem_report_id).first()
    return problem_report


def create_problem_report(db: Session, problem_report_request: ProblemReportRequest):
    db_problem_report = ProblemReport(**problem_report_request.dict())
    db.add(db_problem_report)
    db.commit()
    db.refresh(db_problem_report)
    return db_problem_report


def delete_problem_report(db: Session, problem_report_id: int):
    db_problem_report = db.query(ProblemReport).filter(ProblemReport.id == problem_report_id).first()
    if db_problem_report is None:
        raise Exception()
    db.query(ProblemReport).filter(ProblemReport.id == problem_report_id).delete()
    db.commit()


def create_user(db: Session, user_request: UserRequest):
    db_user_request = User(**user_request.dict())
    db.add(db_user_request)
    db.commit()
    db.refresh(db_user_request)
    return db_user_request


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter_by(id=user_id).first()

    user_response = UserResponse(
        id=user.id,
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        telephone_number=user.telephone_number,
        date_of_birth=user.date_of_birth,
        date_of_registration=user.date_of_registration,
    )
    return user_response


def create_product(db: Session, product_request: ProductRequest):
    db_product = Product(**product_request.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter_by(id=product_id).first()
    return ProductResponse(
        id=product.id,
        user_id=product.user_id,
        title=product.title,
        description=product.description,
        contact_phone=product.contact_phone,
        contact_email=product.contact_email,
        country=product.country,
        city=product.city,
        street=product.street,
        price=product.price
    )


def delete_product(db: Session, product_id: int):
    db.query(Product).filter(Product.id == product_id).delete()
    db.commit()


def get_all_products(db: Session):
    db_product = db.query(Product).all()
    return db_product
