import os
from dotenv import load_dotenv
from flask import jsonify, render_template, make_response, request, flash, url_for, redirect, session
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
from flask_mail import Message
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from models import UserModel
from marshmallow import ValidationError
from schema.schema import UserSchema, LoginSchema, AzureCredentialSchema
from resources.utils import hashPassword, checkPassword
from mail_extension import mail

load_dotenv()
s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))


class UserRegister(Resource):
    def post(self):
        schema = UserSchema()
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        raw_data = {"email":email,"username":username, "password":hashPassword(password)}
        try:
            data = schema.load(raw_data)
        except ValidationError as err:
            return jsonify(err.messages), 422 # check this error message
        
        #avid creating existing user
        if UserModel.find_by_email(data["email"]):
            return {"message":"Email already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        login_user(user=user, force=True)
        return make_response(redirect(url_for('home')))
    
    def get(self):
        return make_response(render_template("signup.html"))

class UserLogin(Resource):
    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")

        schema = LoginSchema()
        data = {"email":email, "password":password}
        
        try:
            data = schema.load(data)
            print(data)
        except ValidationError as err:
            return jsonify(err.messages), 422
        
        user = UserModel.find_by_email(data["email"])
        
        #check password
        if user:
            if checkPassword(data["password"], user.password):
                login_user(user=user, force=True)
                # flash("Login Successful")
                return make_response(redirect(url_for('home')))
                # return {"message": "Login Sucessful","token": access_token}, 200
            else:
                return {"message": "Incorrect password"}, 401
        else:
            return {"message": "User not found"}, 404

    def get(self):
        return make_response(render_template("login.html"))
    
class UserLogout(Resource):
    @login_required
    def get(self):
        logout_user()        
        return redirect(url_for('login'))
    

class ForgotPassword(Resource):
    def post(self):
        email = request.form.get("email")
        user = UserModel.find_by_email(email=email)
        if not user:
            return {'message':"Email not found"}, 404
        token = s.dumps(email, salt='password-reset-salt')
        print(f'Token - {token}')
        msg = Message('Password reset request', sender="mailtrap@demomailtrap.com", recipients=[email])
        link = url_for('resetpassword', token=token, _external=True)
        print(f'Link - {link}')
        msg.body = f'Here is the link to reset your password : {link}'
        mail.send(msg)
        flash("A password reset link has been sent to your email.", "info")
        return {"message":"Token generated"}, 200
    
    def get(self):
        return make_response(render_template('forgot_password.html'))

class ResetPassword(Resource):
    def get(self, token):
        try:
            print(token)
            email = s.loads(token, salt="password-reset-salt", max_age=300)
            print(f'Email - {email}')
            return make_response(render_template("reset_password.html", token=token))
        except SignatureExpired:
            return {"message": "Token has expired"}, 404
        except BadSignature:
            return {"message": "Token is invalid"}, 404
            
    def post(self, token):
        print(f"Token - {token}")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("repeat_password")        
        print(f'New_password - {new_password}')
        print(f'Confirm passoword : {confirm_password}')
        if new_password != confirm_password:
            return {'messsage': "Passwords do not match"}, 400
        
        email = s.loads(token, salt="password-reset-salt", max_age=300)
        user = UserModel.find_by_email(email)
        print(user)
        
        # set new password
        if user:
            user.set_password(new_password)
            flash("Password reset successful", "success")
            return {"message": "Password has been reset successfully"}, 200
        return {"message": "Error!"}, 400



        