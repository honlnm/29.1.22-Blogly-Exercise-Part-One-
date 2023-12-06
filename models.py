from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.string(50), nullable=False)

    last_name = db.Column(db.string(50), nullable=False)

    image_url = db.Column(db.Url, nullable=True, default="https://depositphotos.com/vectors/jewelry-gems.html")