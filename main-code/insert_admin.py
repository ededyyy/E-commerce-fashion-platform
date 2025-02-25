from app import app, db
from app.models import Staff
import hashlib

with app.app_context():
    # function to insert a specific admin account
    def insert_admin_account():
        username = "vogueify_admin0"
        password = "Vogueify@1234!"
        admin_exists = Staff.query.filter_by(username=username).first()

        if not admin_exists:
            password = hashlib.md5(password.encode()).hexdigest()
            new_admin = Staff(username=username, password=password)
            db.session.add(new_admin)
            db.session.commit()
            print(f"Admin account '{username}' created successfully!")
        else:
            print(f"Admin account '{username}' already exists.")

    insert_admin_account()
