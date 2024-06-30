from db import db

class AzureCredentialModel(db.Model):
    __tablename__ = "azure_credentials"

    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    tenant_id = db.Column(db.Integer, nullable=False)
    tenant_secret = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("UserModel", back_populates="azure_credentials")
