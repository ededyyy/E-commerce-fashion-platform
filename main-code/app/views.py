from flask import render_template, request, redirect, url_for
from flask import jsonify, session, abort, make_response
from flask_mail import Message
from app import app, db, mail
import hashlib
import random
from datetime import datetime
from .models import Customer, Staff, Address, Product, Category
from .models import Cart, Order, OrderItem, CartItem
from app.utils import allowed_file, save_uploaded_file
import uuid
import logging
from logging.handlers import RotatingFileHandler
from flask import current_app


# 20 items most in one page
def pagination_20(page, items):
    total = len(items)
    start = (page - 1) * 20
    end = start + 20
    paginatedItems = items[start:end]
    totalPage = (total + 20 - 1) // 20
    pagination_info = {
        'current_page': page,
        'total_pages': totalPage,
        'has_prev': page > 1,
        'has_next': page < totalPage,
    }
    return paginatedItems, pagination_info


# 12 items most in one page
def pagination_12(page, items):
    total = len(items)
    start = (page - 1) * 12
    end = start + 12
    paginatedItems = items[start:end]
    totalPage = (total + 12 - 1) // 12
    pagination_info = {
        'current_page': page,
        'total_pages': totalPage,
        'has_prev': page > 1,
        'has_next': page < totalPage,
    }
    return paginatedItems, pagination_info


# system logging
@app.before_request
def before_first_request():
    if not hasattr(app, 'has_run_before'):
        app.logger.info('Application started')
        app.has_run_before = True


@app.teardown_appcontext
def teardown_appcontext(exception):
    if exception:
        app.logger.error(f'Application error: {str(exception)}')
    app.logger.info('Application shutdown')


# user logging
def log_user_action(user_id, action):
    current_app.logger.info(f'User {user_id} performed action: {action}')


# cookie setting
@app.route('/set_cookie')
def set_cookie():
    resp = make_response("Cookie has been set!")
    resp.set_cookie('username', 'john_doe', max_age=3600)
    return resp


@app.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    if username:
        return f"Hello, {username}!"
    else:
        return "No cookie found!"


@app.route('/delete_cookie')
def delete_cookie():
    resp = make_response("Cookie has been deleted!")
    resp.set_cookie('username', '', max_age=0)

    return resp


# routing for home
@app.route('/')
def home():
    cookie_accepted = request.cookies.get('cookie_accepted') == 'true'
    cookie_declined = request.cookies.get('cookie_declined') == 'true'
    show_banner = not (cookie_accepted or cookie_declined)

    gifting_products = (
        Product.query
        .join(Product.categories)
        .filter(Category.name == 'gifting')
        .limit(3)
        .all()
    )

    return render_template(
        'home.html',
        gifting_products=gifting_products,
        show_banner=show_banner
    )


# routing for gifting
@app.route('/gifting')
def gifting():
    products = (
        Product.query
        .join(Product.categories).filter(Category.name == 'gifting').all())
    page = request.args.get('page', type=int, default=1)
    paginated_products, pagination_info = pagination_12(page, products)
    return render_template('gifting.html',
                           products=paginated_products,
                           active_page='gifting', pagination=pagination_info)


# routing for handbags
@app.route('/handbags')
def handbags():
    products = (Product.query
                .join(Product.categories)
                .filter(Category.name == 'handbags').all())
    page = request.args.get('page', type=int, default=1)
    paginated_products, pagination_info = pagination_12(page, products)
    return render_template('handbags.html',
                           products=paginated_products,
                           active_page='handbags', pagination=pagination_info)


# routing for clothing
@app.route('/clothing')
def clothing():
    products = (Product.query
                .join(Product.categories)
                .filter(Category.name == 'clothing').all())
    page = request.args.get('page', type=int, default=1)
    paginated_products, pagination_info = pagination_12(page, products)
    return render_template('clothing.html',
                           products=paginated_products,
                           active_page='clothing',
                           pagination=pagination_info)


# routing for accessories
@app.route('/accessories')
def accessories():
    products = (Product.query
                .join(Product.categories)
                .filter(Category.name == 'accessories').all())
    page = request.args.get('page', type=int, default=1)
    paginated_products, pagination_info = pagination_12(page, products)
    return render_template('accessories.html', products=paginated_products,
                           active_page='accessories',
                           pagination=pagination_info)


# routing for jewellery
@app.route('/jewellery')
def jewellery():
    products = (Product.query
                .join(Product.categories)
                .filter(Category.name == 'jewellery').all())
    page = request.args.get('page', type=int, default=1)
    paginated_products, pagination_info = pagination_12(page, products)
    return render_template('jewellery.html',
                           products=paginated_products,
                           active_page='jewellery', pagination=pagination_info)


# preprocess
def preprocess_string(s):
    return s.replace(" ", "").lower()


# for kmp search
def compute_lps_array(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    if not pattern:
        return True
    lps = compute_lps_array(pattern)
    i = 0
    j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == len(pattern):
                return True
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False


# routing for search
@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    if query:
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    else:
        products = []

    page = request.args.get('page', type=int, default=1)
    paginated_products, pagination_info = pagination_12(page, products)

    return render_template('search.html',
                           products=paginated_products,
                           query=query, pagination=pagination_info)


# routing for register
@app.route('/Register', methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    if request.method == "POST":
        data = request.json
        username = data.get('username')
        password = data.get('password')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        register_date = datetime.now().date()
        if Customer.query.filter_by(username=username).first():
            log_user_action(None,f"Failed registration attempt - Username {username} already exists")
            return jsonify({"success": False,"message": "There already exists same username"}), 400
        password = hashlib.md5(password.encode()).hexdigest()
        customer = Customer(username=username,
                            password=password,
                            firstname=firstname,
                            lastname=lastname,
                            email=email,
                            register_date=register_date)
        db.session.add(customer)
        db.session.commit()
        log_user_action(customer.id, f"New user registered - Username: {username}, Email: {email}")
        # successfully register
        return jsonify({"success": True,
                        "message": f"Welcome, {username}!"}), 200


# check the email in database
@app.route('/check_email', methods=["POST"])
def check_email():
    email = request.json.get('email')
    action = request.json.get('action')

    customer = Customer.query.filter_by(email=email).first()

    if action == "register":
        # for register
        if customer:
            return jsonify({"exists": True,
                            "message": "This email is already registered."}), 400
        else:
            return jsonify({"exists": False,
                            "message": "Email is available."}), 200
    elif action == "login":
        # for log in
        if customer:
            return jsonify({"exists": True,
                            "message": "Email is registered."}), 200
        else:
            return jsonify({"exists": False,
                            "message": "Email does not exist. Please register."}), 
    else:
        return jsonify({"exists": False, "message": "Invalid action."}), 400


# send email message function
@app.route('/send_mail', methods=["POST"])
def send_mail():
    email = request.json.get('email')
    verification_code = str(random.randint(10000, 99999))
    session['verification_code'] = verification_code
    message = Message(subject="Vogueify",
                      recipients=[email],
                      body=f"Your verification code is: {verification_code}")
    mail.send(message)
    return jsonify({"success": True,
                    "message": "Verification code sent successfully."}), 200


# vefify the code
@app.route('/verify_code', methods=["POST"])
def verify_code():
    user_code = request.json.get('code')
    stored_code = session.get('verification_code')
    if user_code == stored_code:
        return jsonify({"success": True,
                        "message": "Verification code is correct."}), 200
    else:
        return jsonify({"success": False,
                        "message": "Verification code is incorrect."}), 400


# routing for account page
@app.route('/account')
def account():
    if 'customer_id' not in session:
        return redirect(url_for('log_in_password'))
    customer = Customer.query.get(session['customer_id'])
    return render_template('account.html', customer=customer)


# routing for cart page
@app.route('/cart')
def cart():
    if 'customer_id' not in session:
        return redirect(url_for('log_in_password'))
    customer = Customer.query.get(session['customer_id'])
    return render_template('cart.html', customer=customer)


# routing for order page
@app.route('/order')
def order():
    if 'customer_id' not in session:
        return redirect(url_for('log_in_password'))

    customer = Customer.query.get(session['customer_id'])
    status_filter = request.args.get('status', 'all')

    base_query = Order.query.filter(
        (Order.customer_id == customer.id) &
        ~((Order.status == 'Completed') & (Order.is_deleted == True))
    )

    if status_filter != 'all':
        base_query = base_query.filter_by(status=status_filter)

    orders = base_query.all()

    return render_template('order.html',
                           customer=customer,
                           orders=orders, status_filter=status_filter)


# routing for 404 unfound
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404error.html'), 404


# sign in with password function
@app.route('/log_in_password', methods=["POST", "GET"])
def log_in_password():
    if request.method == "GET":
        return render_template('customer_login_password.html')
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        customer = Customer.query.filter_by(email=email).first()
        # check if there exists customer
        if customer and customer.password == hashed_password:
            session['customer_id'] = customer.id
            session['username'] = customer.username
            log_user_action(customer.id, f"User logged in - Email: {email}")
            return jsonify({"status": "success",
                            "message": f"Welcome, {customer.username}!"}), 200
        else:
            log_user_action(None, f"Failed login attempt - Email: {email}")
            return jsonify({"status": "error",
                            "message": "Invalid email or password, please try again."}), 401


# sign in with email code
@app.route('/login_with_code', methods=["GET", "POST"])
def login_with_code():
    if request.method == "GET":
        return render_template('customer_login_code.html')
    elif request.method == "POST":
        email = request.form.get('email')
        code = request.form.get('code')
        stored_code = session.get('verification_code')

        if code == stored_code:
            customer = Customer.query.filter_by(email=email).first()
            if customer:
                session['customer_id'] = customer.id
                session['username'] = customer.username
                log_user_action(customer.id, f"User logged in with verification code - Email: {email}")
                return jsonify({"status": "success",
                                "message": f"Welcome, {customer.username}!"}), 200
            else:
                log_user_action(None, f"Failed login attempt - Email not found: {email}")
                return jsonify({"status": "error",
                                "message": "Email does not exist. Please register."}), 401
        else:
            log_user_action(None, f"Failed login attempt - Invalid verification code for email: {email}")
            return jsonify({"status": "error",
                            "message": "Invalid verification code. Please try again."}), 401


# update customer info
@app.route('/update_user', methods=["POST"])
def update_user():
    if 'customer_id' not in session:
        return jsonify({"status": "error",
                        "message": "User not logged in."}), 401

    customer_id = session['customer_id']
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({"status": "error", "message": "User not found."}), 404

    username = request.form.get('username')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')

    existing_username = Customer.query.filter_by(username=username).first()
    if existing_username and existing_username.id != customer_id:
        return jsonify({"status": "error",
                        "message": "Username already exists."}), 400

    customer.username = username
    customer.firstname = firstname
    customer.lastname = lastname

    db.session.commit()

    return jsonify({"status": "success",
                    "message": "User information updated successfully."}), 200


# update email
@app.route('/update_email', methods=["POST"])
def update_email():
    if 'customer_id' not in session:
        return jsonify({"status": "error",
                        "message": "User not logged in."}), 401

    customer_id = session['customer_id']
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({"status": "error", "message": "User not found."}), 404

    email = request.form.get('email')

    existing_email = Customer.query.filter_by(email=email).first()
    if existing_email and existing_email.id != customer_id:
        return jsonify({"status": "error",
                        "message": "Email already exists."}), 400

    customer.email = email
    db.session.commit()

    return jsonify({"status": "success",
                    "message": "Email updated successfully."}), 200


# update password
@app.route('/update_password', methods=["POST"])
def update_password():
    if 'customer_id' not in session:
        return jsonify({"status": "error",
                        "message": "User not logged in."}), 401

    customer_id = session['customer_id']
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({"status": "error", "message": "User not found."}), 404

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    if hashlib.md5(current_password.encode()).hexdigest() != customer.password:
        return jsonify({"status": "error",
                        "message": "Current password is incorrect."}), 400

    customer.password = hashlib.md5(new_password.encode()).hexdigest()
    db.session.commit()

    return jsonify({"status": "success",
                    "message": "Password updated successfully."}), 200


# to get address
@app.route('/api/address/<int:address_id>', methods=['GET'])
def get_address(address_id):
    address = Address.query.filter_by(id=address_id, is_deleted=False).first()
    if not address:
        return jsonify({"error": "Address not found"}), 404

    return jsonify({
        "id": address.id,
        "country": address.country,
        "province": address.province,
        "city": address.city,
        "street": address.street,
    }), 200


# for add address
@app.route('/add_address', methods=['POST'])
def add_address():
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.form
    customer = Customer.query.get(session['customer_id'])

    existing_address = Address.query.filter(
        db.func.lower(Address.country) == db.func.lower(data.get('country')),
        db.func.lower(Address.province) == db.func.lower(data.get('province')),
        db.func.lower(Address.city) == db.func.lower(data.get('city')),
        db.func.lower(Address.street) == db.func.lower(data.get('street'))
    ).first()

    if existing_address:
        if existing_address.is_deleted:
            existing_address.is_deleted = False
            db.session.commit()
            return jsonify({"success": True,
                            "message": "Address restored successfully"}), 200
        else:
            return jsonify({"success": False,
                            "message": "Address already exists."}), 400
    else:
        address = Address(
            country=data.get('country'),
            province=data.get('province'),
            city=data.get('city'),
            street=data.get('street')
        )
        db.session.add(address)
        db.session.commit()

        customer.addresses.append(address)
        db.session.commit()

        return jsonify({"success": True,
                        "message": "Address added successfully"}), 200


# for update address
@app.route('/update_address', methods=['POST'])
def update_address():
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.form
    address = Address.query.get(data.get('address_id'))
    if not address:
        return jsonify({"success": False, "message": "Address not found"}), 404

    existing_address = Address.query.filter(
        db.func.lower(Address.country) == db.func.lower(data.get('country')),
        db.func.lower(Address.province) == db.func.lower(data.get('province')),
        db.func.lower(Address.city) == db.func.lower(data.get('city')),
        db.func.lower(Address.street) == db.func.lower(data.get('street')),
        Address.id != address.id
    ).first()

    if existing_address:
        if existing_address.is_deleted:
            existing_address.is_deleted = False
            db.session.commit()
            return jsonify({"success": True,
                            "message": "Address restored successfully"}), 200
        else:
            return jsonify({"success": False,
                            "message": "Address already exists."}), 400
    else:
        address.country = data.get('country')
        address.province = data.get('province')
        address.city = data.get('city')
        address.street = data.get('street')
        db.session.commit()
        return jsonify({"success": True,
                        "message": "Address updated successfully"}), 200


# for delete address
@app.route('/delete_address/<int:address_id>', methods=['POST'])
def delete_address(address_id):
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    try:
        address = Address.query.get(address_id)
        if not address:
            return jsonify({'status': 'error', 'message': 'Address not found'}), 404
        address.is_deleted = True
        db.session.commit()
        return jsonify({"success": True,
                        "message": "Address deleted successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500


# for customer log out
@app.route('/logout')
def logout():
    session.pop('customer_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))


# to show the product details
@app.route('/api/products/<int:id>', methods=['GET'])
def get_product_details(id):
    product = Product.query.get(id)
    if product:
        return jsonify({
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock_quantity': product.stock_quantity,
            'categories': [category.name for category in product.categories],
            'img_url': product.img_url
        })
    else:
        return jsonify({'error': 'Product not found'}), 404


# add products to cart
@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    # check if logged in
    if 'customer_id' not in session:
        return jsonify({"success": False,
                        "message": "Please log in first"}), 401

    data = request.get_json()
    product_id = data.get('productId')
    customer_id = session.get('customer_id')

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404

    cart = Cart.query.filter_by(customer_id=customer_id).first()
    if not cart:
        cart = Cart(customer_id=customer_id)
        db.session.add(cart)
        db.session.commit()

    cart_item = (CartItem.query
                 .filter_by(cart_id=cart.id, product_id=product_id).first())
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id,
                             product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    log_user_action(customer_id, f"Product added to cart - Product ID: {product_id}, Quantity: {cart_item.quantity}")
    return jsonify({"success": True, "message": "Product added to cart"}), 200


# can update product number in cart
@app.route('/api/cart/update/<int:item_id>', methods=['POST'])
def update_cart_item(item_id):
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.get_json()
    quantity = data.get('quantity', 1)

    cart_item = CartItem.query.get(item_id)
    if not cart_item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    cart_item.quantity = quantity
    db.session.commit()

    # return the total price
    total_price = cart_item.product.price * cart_item.quantity
    return jsonify({
        "success": True,
        "message": "Quantity updated",
        "total_price": total_price
    }), 200


# can delete product
@app.route('/api/cart/remove/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    cart_item = CartItem.query.get(item_id)
    if not cart_item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"success": True, "message": "Item removed"}), 200


# fetch the products in cart
@app.route('/api/cart/items', methods=['GET'])
def get_cart_items():
    if 'customer_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    cart = Cart.query.filter_by(customer_id=session['customer_id']).first()
    if not cart:
        return jsonify([]), 200

    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    items = [{"product_id": item.product_id, "quantity": item.quantity} for item in cart_items]
    return jsonify(items), 200


# can check the number of stock
@app.route('/api/product/stock/<int:item_id>', methods=['GET'])
def get_product_stock(item_id):
    product = Product.query.get(item_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"stock": product.stock_quantity}), 200


# can check out
@app.route('/checkout', methods=['POST'])
def checkout():
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    data = request.json
    selected_items = data.get('items', [])
    address_id = data.get('address_id')

    if not selected_items:
        return jsonify({"success": False, "message": "No items selected"}), 400

    if not address_id:
        return jsonify({"success": False,
                        "message": "Address not selected"}), 400

    customer = Customer.query.get(session['customer_id'])
    if not customer:
        return jsonify({"success": False,
                        "message": "Customer not found"}), 404
    # caculate the total price
    total_price = 0
    order_items = []
    for item in selected_items:
        cart_item = CartItem.query.get(item['id'])
        if not cart_item:
            return jsonify({"success": False,
                            "message": "Item not found"}), 404
        total_price += cart_item.product.price * int(item['quantity'])
        order_items.append({
            'product_id': cart_item.product.id,
            'quantity': int(item['quantity']),
            'price': cart_item.product.price
        })
    # create order
    order = Order(
        total_price=total_price,
        order_number=str(uuid.uuid4())[:8],
        status='Pending Payment',
        customer_id=customer.id,
        address_id=address_id
    )
    db.session.add(order)
    db.session.commit()
    # create order_item
    for item in order_items:
        order_item = OrderItem(
            quantity=item['quantity'],
            price=item['price'],
            product_id=item['product_id'],
            order_id=order.id
        )
        db.session.add(order_item)
        db.session.commit()
    log_user_action(customer.id, f"Order placed - Order ID: {order.id}, Total Price: {total_price}")
    return jsonify({"success": True, "order_id": order.id}), 200


# can delete order
@app.route('/remove_order/<int:order_id>', methods=['POST'])
def remove_order(order_id):
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    order = Order.query.get(order_id)
    if not order or order.customer_id != session['customer_id']:
        return jsonify({"success": False, "message": "Order not found"}), 404

    try:
        if order.status == 'Pending Payment':
            for order_item in order.items:
                db.session.delete(order_item)
            db.session.delete(order)
        elif order.status == 'Completed':
            order.is_deleted = True
        db.session.commit()

        return jsonify({"success": True,
                        "message": "Order removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# can pay the order
@app.route('/pay_order/<int:order_id>', methods=['POST'])
def pay_order(order_id):
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    order = Order.query.get(order_id)
    if not order or order.customer_id != session['customer_id']:
        return jsonify({"success": False, "message": "Order not found"}), 404
    try:
        for order_item in order.items:
            product = Product.query.get(order_item.product_id)
            if not product:
                return jsonify({"success": False,
                                "message": f"Product {order_item.product_id} not found"}), 404

            if product.stock_quantity < order_item.quantity:
                return jsonify({"success": False, "message": f"Insufficient stock for product {product.name}"}), 400

            product.stock_quantity -= order_item.quantity
            db.session.add(product)

        order.status = 'Pending Shipment'
        db.session.commit()
        current_app.logger.info(f"Order paid successfully - Order ID: {order_id}, Customer ID: {session['customer_id']}")
        return jsonify({"success": True, "message": "Payment successful"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# for refund and return
@app.route('/refund_and_return/<int:order_id>', methods=['POST'])
def refund_and_return(order_id):
    if 'customer_id' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    order = Order.query.get(order_id)
    if not order or order.customer_id != session['customer_id']:
        return jsonify({"success": False, "message": "Order not found"}), 404

    try:
        # update the status as "refund and return"
        order.status = 'Refund and Return'
        db.session.commit()
        current_app.logger.info(f"Refund requested - Order ID: {order_id}, Customer ID: {session['customer_id']}")
        return jsonify({"success": True, "message": "Refund and return request submitted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# for confirm receipt
@app.route('/confirm-receipt/<int:order_id>', methods=['POST'])
def confirm_receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status == 'In Transit':
        order.status = 'Completed'
        db.session.commit()
        current_app.logger.info(f"Order receipt confirmed - Order ID: {order_id}, Customer ID: {order.customer_id}")
        return jsonify(success=True)
    return jsonify(success=False, message='Invalid order status')


# sign in for admin function
@app.route('/sign_in_admin', methods=["POST"])
def sign_in_admin():
    if request.method == "POST":
        username = request.form.get('admin_username')
        password = request.form.get('admin_password')
        admin = Staff.query.filter_by(username=username).first()
        if admin and admin.password == hashlib.md5(password.encode()).hexdigest():
            # log in successfully
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return jsonify({"success": True,
                            "message": "Admin login successful!"}), 200
        else:
            # fail to log in
            return jsonify({"success": False,
                            "message": "Invalid username or password"}), 401


# sign out for admin
@app.route('/logout_admin', methods=['POST'])
def logout_admin():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect(url_for('home'))


# for admin product management
@app.route('/admin_product_management')
def admin_product_management():
    if not session.get('admin_logged_in'):
        abort(404)
    products = Product.query.all()
    categories = Category.query.all()
    page = request.args.get('page', type=int, default=1)
    paginated_products, pagination_info = pagination_12(page, products)
    return render_template('admin_product_management.html',
                           products=paginated_products,
                           categories=categories, pagination=pagination_info)


# for admin order management
@app.route('/admin_order_management')
def admin_order_management():
    if not session.get('admin_logged_in'):
        abort(404)
    orders = Order.query.all()
    return render_template('admin_order_management.html', orders=orders)


# for admin customer management
@app.route('/admin_customer_management')
def admin_customer_management():
    if not session.get('admin_logged_in'):
        abort(404)
    customers = Customer.query.all()
    return render_template('admin_customer_management.html',
                           customers=customers)


# can add product
@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    stock_quantity = request.form.get('stock_quantity')
    img_file = request.files.get('img_file')
    category_ids = request.form.getlist('category_ids[]')

    if not category_ids:
        return jsonify({'status': 'error',
                        'message': 'Please select at least one category.'})

    existing_product = Product.query.filter_by(name=name).first()
    if existing_product:
        return jsonify({'status': 'error',
                        'message': 'Product name already exists. Please choose a different name.'})

    if not allowed_file(img_file.filename):
        return jsonify({'status': 'error',
                        'message': 'Invalid file type. Please upload an image file.'})

    filename = save_uploaded_file(img_file)
    if not filename:
        return jsonify({'status': 'error',
                        'message': 'Failed to save the file.'})

    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        img_url=url_for('static', filename=f'img/{filename}')
    )

    for category_id in category_ids:
        category = Category.query.get(category_id)
        if category:
            new_product.categories.append(category)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({'status': 'success',
                    'message': 'Product added successfully!'})


# can edit product information
@app.route('/edit_product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'status': 'error',
                        'message': 'Product not found'}), 404

    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    stock_quantity = request.form.get('stock_quantity')
    img_file = request.files.get('img_file')
    category_ids = request.form.getlist('category_ids[]')

    # check if exists the same product name
    existing_product = (Product.query
                        .filter(Product.name == name, Product.id != product_id)
                        .first())
    if existing_product:
        return jsonify({'status': 'error',
                        'message': 'Product name already exists. Please choose a different name.'})

    product.name = name
    product.description = description
    product.price = price
    product.stock_quantity = stock_quantity

    img_file = request.files.get('img_file')
    if img_file and img_file.filename != '':
        if not allowed_file(img_file.filename):
            return jsonify({'status': 'error',
                            'message': 'Invalid file type. Please upload an image.'})
        filename = save_uploaded_file(img_file)
        if not filename:
            return jsonify({'status': 'error',
                            'message': 'Failed to save the file.'})
        product.img_url = url_for('static', filename=f'img/{filename}')

    category_ids = request.form.getlist('category_ids[]')
    product.categories = (Category.query
                          .filter(Category.id.in_(category_ids)).all())

    db.session.commit()

    return jsonify({'status': 'success',
                    'message': 'Product updated successfully!'})


# can delete product
@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if not session.get('admin_logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'status': 'error',
                        'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'Product deleted successfully!',
        'redirect_url': url_for('admin_product_management', page=1)
    })


# can change order status as in transit
@app.route('/ship-order/<int:order_id>', methods=['POST'])
def ship_order(order_id):
    order = Order.query.get_or_404(order_id)

    if order.status == 'Pending Shipment':
        try:
            for order_item in order.items:
                product = Product.query.get(order_item.product_id)
                if not product:
                    return jsonify({"success": False, "message": f"Product {order_item.product_id} not found"}), 404

                if product.stock_quantity < order_item.quantity:
                    return jsonify({"success": False, "message": f"Insufficient stock for product {product.name}"}), 400

                product.stock_quantity -= order_item.quantity
                db.session.add(product)
            order.status = 'In Transit'
            db.session.commit()
            current_app.logger.info(f"Order shipped - Order ID: {order_id}, Stock reduced")
            return jsonify(success=True)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to ship order - Error: {str(e)}")
            return jsonify(success=False, message=str(e)), 500
    else:
        return jsonify(success=False, message='Invalid order status')


# can confirm refund and return request
@app.route('/process_refund/<int:order_id>', methods=['POST'])
def process_refund(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != 'Refund and Return':
        return jsonify({"success": False,
                        "message": "Invalid order status"}), 400

    data = request.get_json()
    accept_refund = data.get('accept_refund')
    reject_reason = data.get('reject_reason')

    try:
        if accept_refund:
            for order_item in order.items:
                product = Product.query.get(order_item.product_id)
                if not product:
                    return jsonify({"success": False, "message": f"Product {order_item.product_id} not found"}), 404

                product.stock_quantity += order_item.quantity
                db.session.add(product)

        order.refund_processed = True
        order.refund_accepted = accept_refund
        if not accept_refund:
            order.refund_reject_reason = reject_reason
        db.session.commit()

        current_app.logger.info(f"Refund processed - Order ID: {order_id}, Accepted: {accept_refund}, Stock updated")
        return jsonify({"success": True,
                        "message": "Refund processed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to process refund - Error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
