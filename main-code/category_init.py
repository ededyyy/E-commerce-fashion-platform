from app import app, db
from app.models import Category


def add_fixed_categories():
    """Initialize fixed categories if they don't already exist."""
    fixed_categories = ["clothing", "handbags",
                        "accessories", "jewellery", "gifting"]
    for name in fixed_categories:
        category = Category.query.filter_by(name=name).first()
        if not category:
            category = Category(name=name)
            db.session.add(category)
            print(f"Category '{name}' added successfully!")
        else:
            print(f"Category '{name}' already exists.")
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        add_fixed_categories()
