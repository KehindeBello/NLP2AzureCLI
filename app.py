import os
from dotenv import load_dotenv
from flask_mail import Message
from db import db
from flask import Flask, make_response, render_template, session
from flask_login import LoginManager, login_required
from mail_extension import mail
from routes.routes import create_routes
from models import UserModel

load_dotenv()

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'
app.config["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
app.config["SQLALCHEMY_DATABASE_URI"]= os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
app.config["JWT_SECRET_KEY"]= os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"]= os.getenv("JWT_TOKEN_LOCATION")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = '457952ba709ee67e02480c4b83d7fb45'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

loginManager = LoginManager(app=app)
mail.init_app(app)
db.init_app(app)

api = create_routes(app)

with app.app_context():
    db.create_all()

@loginManager.user_loader
def load_user(email):
    return UserModel.query.get(email)

@app.get('/')
def index():
    return render_template('index.html')


@app.get("/home")
@login_required
def home():
    return make_response(render_template("homepage.html"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)