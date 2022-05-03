from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, login_required

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'e8iE3$n#g%wxVKa%NtUDFT9czTMiFd'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




from twitterbot import routes
