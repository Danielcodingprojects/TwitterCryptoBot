from twitterbot import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class FollowerCount(db.Model):
    __tablename__ = "follower_count"
    datetime = db.Column(db.DateTime, primary_key=True)
    count = db.Column(db.Integer, nullable=False)


class Tweets(db.Model):
    __tablename__ = "tweet"
    tweet_id = db.Column(db.Integer, primary_key=True)
    tweet_body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    blockchain = db.Column(db.String(255), nullable=False)
    coin = db.Column(db.String(255), nullable=False)
    amount_crypto = db.Column(db.Integer, nullable=False)
    amount_usd = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(255), nullable=False)
    from_addr = db.Column(db.String(255), nullable=False)
    to_addr = db.Column(db.String(255), nullable=False)


class Pagination_Key(db.Model):
    __tablename__ = "pagination_key"
    cursor = db.Column(db.String(255), primary_key=True)
