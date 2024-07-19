import os
from dotenv import load_dotenv
from flask import redirect, request, session
from flask_restful import Resource, reqparse
import requests

load_dotenv()

tenant_id = os.getenv("tenant_id")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_uri")

authorize_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"


class RunCommandInCli(Resource):
    def get(self):
        auth_url = f"{authorize_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=https%3A%2F%2Fmanagement.azure.com%2Fuser_impersonation"
        return redirect(auth_url)

class Callback(Resource):
    def get(self):
        code = request.args.get('code')
        if not code:
            return {'error': 'Authorization code not provided'}, 400
        
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return {'error': 'Failed to retrieve access token'}, 400
        
        session['access_token'] = token_json['access_token']
        session['refresh_token'] = token_json['refresh_token']
        
        return {'message': 'Login successful'}, 200

