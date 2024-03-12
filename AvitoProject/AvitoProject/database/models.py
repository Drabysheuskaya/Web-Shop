from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Date, BLOB, Table, LargeBinary


product_category = Table('ProductCategory', Base.metadata,
                         Column('product_id', Integer, ForeignKey('Product.id')),
                         Column('category_id', Integer, ForeignKey('Category.id'))
                         )

liked_products = Table('LikedProduct', Base.metadata,
                       Column('product_id', Integer, ForeignKey('Product.id')),
                       Column('user_id', Integer, ForeignKey("User.id")))


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    telephone_number = Column(String(30), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    date_of_registration = Column(DateTime, nullable=False, default=datetime.now)
    products = relationship('Product', back_populates='user')
    liked_prod = relationship('Product', secondary=liked_products, back_populates='liking_users')
    problem_reports = relationship('ProblemReport', back_populates='user')


class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    title = Column(String(30), nullable=False)
    description = Column(String(300), nullable=False)
    date_of_publishing = Column(DateTime, nullable=False, default=datetime.now)
    contact_phone = Column(String(30), nullable=False)
    contact_email = Column(String(30), nullable=False)
    country = Column(String(30), nullable=False)
    city = Column(String(30), nullable=False)
    street = Column(String(30), nullable=False)
    price = Column(Float, nullable=False)
    user = relationship('User', back_populates='products')
    images = relationship('Image', back_populates='product')
    categories = relationship('Category', secondary=product_category, back_populates='products')
    liking_users = relationship('User', secondary=liked_products, back_populates='liked_prod')
    problem_reports = relationship('ProblemReport', back_populates='product')


class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(20), nullable=False)
    products = relationship('Product', secondary=product_category, back_populates='categories')


class Image(Base):
    __tablename__ = 'Image'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    image = Column(LargeBinary, nullable=False)
    product_id = Column(Integer, ForeignKey('Product.id'))
    product = relationship('Product', back_populates='images')


class ProblemReport(Base):
    __tablename__ = 'ProblemReport'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    description = Column(String(200), nullable=False)
    date_of_publishing = Column(DateTime, nullable=False, default=datetime.now)
    product_id = Column(Integer, ForeignKey('Product.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    product = relationship('Product', back_populates='problem_reports')
    user = relationship('User', back_populates='problem_reports')



