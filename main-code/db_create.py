from config import SQLALCHEMY_DATABASE_URI  # noqa: E402, F401
from app import db, app

with app.app_context():
    db.create_all()
