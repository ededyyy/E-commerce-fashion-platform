from app import db
from sqlalchemy import Enum


# Association table for many-to-many relationship between Product and Category
product_category = db.Table(
    'product_category',
    db.Column('product_id',
              db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer,
              db.ForeignKey('categories.id'), primary_key=True)
)

# Association table for many-to-many relationship between Customer and Address
customer_address = db.Table(
    'customer_address',
    db.Column('customer_id',
              db.Integer, db.ForeignKey('customers.id'), primary_key=True),
    db.Column('address_id', db.Integer,
              db.ForeignKey('addresses.id'), primary_key=True)
)


# custimer model
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    register_date = db.Column(db.Date, nullable=False,
                              default=db.func.current_date())

    # Many-to-many relationship with Address
    addresses = db.relationship('Address', secondary=customer_address,
                                back_populates='customers', lazy=True)

    # Other relationships
    cart = db.relationship('Cart', back_populates='customer',
                           lazy=True, uselist=False)
    orders = db.relationship('Order', back_populates='customer', lazy=True)

    def __repr__(self):
        return "Customer:%s" % self.username


# seller staff model (admin at the same time)
class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)


# address model
class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(200), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    # Many-to-many relationship with Customer
    customers = db.relationship('Customer',
                                secondary=customer_address,
                                back_populates='addresses', lazy=True)

    # Relationship with Order
    orders = db.relationship('Order', back_populates='address', lazy=True)


# product model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.String(500))
    img_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False,
                           default=db.func.current_timestamp())

    # relationship with category model
    categories = db.relationship('Category', secondary=product_category,
                                 back_populates='products', lazy=True)

    # relationship with orderitem
    order_items = db.relationship('OrderItem', back_populates='product',
                                  cascade='all, delete-orphan')

    # relationship between cart item
    cart_items = db.relationship('CartItem', back_populates='product',
                                 cascade='all, delete-orphan', lazy=True)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # relationship with product model
    products = db.relationship('Product', secondary=product_category,
                               back_populates='categories', lazy=True)


# cart model
class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),
                            nullable=False)
    number = db.Column(db.Integer, default=0)

    # relationship with customer model
    customer = db.relationship('Customer', back_populates='cart', lazy=True)

    # relationship with cart item
    items = db.relationship('CartItem', back_populates='cart', lazy=True)

    def __repr__(self):
        return "Cart:%s" % self.number


# cart item model
class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    # relatiobship between cart
    cart = db.relationship('Cart', back_populates='items', lazy=True)

    # relationship between product
    product = db.relationship('Product',
                              back_populates='cart_items', lazy=True)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(Enum('Pending Payment',
                            'Pending Shipment',
                            'In Transit',
                            'Completed',
                            'Refund and Return',
                            name='order_status'), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False,
                            default=db.func.current_timestamp())
    refund_processed = db.Column(db.Boolean, default=False, nullable=False)
    refund_accepted = db.Column(db.Boolean, default=None, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    refund_reject_reason = db.Column(db.String(500), nullable=True)

    # relationship with address model
    address_id = db.Column(db.Integer,
                           db.ForeignKey('addresses.id'), nullable=False)
    address = db.relationship('Address', back_populates='orders', lazy=True)

    # relationship with customer model
    customer_id = db.Column(db.Integer,
                            db.ForeignKey('customers.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='orders', lazy=True)

    # relationship with orderItem model
    items = db.relationship('OrderItem', back_populates='order', lazy=True)


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # relationship with product model
    product_id = db.Column(db.Integer,
                           db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product',
                              back_populates='order_items', lazy=True)

    # relationship with order model
    order_id = db.Column(db.Integer,
                         db.ForeignKey('orders.id'), nullable=False)
    order = db.relationship('Order', back_populates='items', lazy=True)
