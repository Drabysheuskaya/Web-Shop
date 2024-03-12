from sqlalchemy.orm import Session
from database.models import Product


def get_images_of_product(db: Session, product_id: int):
    product = db.query(Product).get(product_id)
    if product:
        image_ids = [image.id for image in product.images]
        return image_ids
    return []


def get_images_of_product_description(db: Session, product_id: int):
    product = db.query(Product).get(product_id)
    if product:
        images = []
        for index, image in enumerate(product.images):
            preview_image = True if index == 0 else False
            images.append({
                "id": image.id,
                "previewImage": preview_image
            })
        return images
    return []
