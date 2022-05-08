from twitterbot import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class FollowerCount(db.Model):
    __tablename__ = "follower_count"
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)


class Tweets(db.Model):
    # TODO; Make db to store send tweets in
    pass
