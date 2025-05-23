import os
from dotenv import load_dotenv
from db import db
from flask import Flask, make_response, render_template
from flask_login import LoginManager, login_required, current_user
from flask_cors import CORS
from routes.routes import create_routes
from models import UserModel

load_dotenv()

app = Flask(__name__)
CORS(app)

app.secret_key = os.getenv("SECRET_KEY")
app.config["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
app.config["SQLALCHEMY_DATABASE_URI"]= os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
app.config["JWT_SECRET_KEY"]= os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"]= os.getenv("JWT_TOKEN_LOCATION")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


loginManager = LoginManager(app=app)
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
    return make_response(render_template("homepage.html", user_name=current_user.username))

if __name__ == '__main__':
    app.run(port=5000, debug=True)