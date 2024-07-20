from db import db
from resources.utils import hashPassword
from flask_login import UserMixin

class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    azure_credentials = db.relationship("AzureCredentialModel", back_populates="user", lazy="dynamic",cascade="all, delete-orphan")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def set_password(self, password):
        self.password = hashPassword(password=password)
        db.session.commit()        