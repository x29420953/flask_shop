import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    birth = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    deleted_at = db.Column(db.DateTime)
    is_super = db.Column(db.Integer, default=1)

    db_user_order = db.relationship("Order", backref="user")
    db_user_totalorder = db.relationship("TotalOrder", backref="user")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return "{}".format(self.id)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    classify = db.Column(db.String(100), nullable=False)
    deleted_at = db.Column(db.DateTime)

    db_product_productimg = db.relationship("ProductImg", backref="product")
    db_product_order = db.relationship("Order", backref="product")


class ProductImg(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    url = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    deleted_at = db.Column(db.DateTime)


class TotalOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    status = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    total_count = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    update_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    price = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    deleted_at = db.Column(db.DateTime)
    total_order_id = db.Column(db.Integer)

