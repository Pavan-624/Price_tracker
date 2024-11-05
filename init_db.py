# init_db.py
from app import app, db

def initialize_db():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    initialize_db()
