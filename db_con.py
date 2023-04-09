from flask_sqlalchemy import SQLAlchemy
import os


db = None


def db_init(app):
    global db
    db = SQLAlchemy(app)
    from models import Admin
    if not os.path.exists('instance/base2'):
        db.create_all()
    return db

