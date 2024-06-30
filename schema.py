from marshmallow import Schema, fields

class UserSchema(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class AzureCredentialSchema(Schema):
    subscription_id = fields.Int(required=True)
    tenant_id = fields.Int(required=True)
    tenant_secret = fields.Int(required=True)
    client_id = fields.Int(required=True)

