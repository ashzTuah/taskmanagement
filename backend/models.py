from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    # id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="user")

    tasks = db.relationship("Task", backref="user", lazy=True)


class Task(db.Model):
    __tablename__ = "tasks"

    # id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="pending")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)