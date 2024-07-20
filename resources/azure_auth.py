import os
import subprocess
# from dotenv import load_dotenv
from flask import jsonify, make_response, render_template, request, session
from flask_restful import Resource
# import requests

# load_dotenv()

# tenant_id = os.getenv("tenant_id")
# client_id = os.getenv("client_id")
# client_secret = os.getenv("client_secret")
# redirect_uri = os.getenv("redirect_uri")

# authorize_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
# token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')

class AuthAzure(Resource):
    def get(self):
        # auth_url = f"{authorize_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&response_mode=query&scope=https%3A%2F%2Fmanagement.azure.com%2Fuser_impersonation"
        # return redirect(auth_url)
        return make_response(render_template("credentials.html"))
    
    def post(self):
        azure_cli_command = request.args.get("command")
        return render_template('credentials.html', azureCliCommand = azure_cli_command)
    
    
class RunCommand(Resource):
    def post(self):
        data = request.json
        print(data)
        client_id = data["clientId"]
        client_secret = data["clientSecret"]
        tenant_id = data["tenantId"]
        command = data["command"]

        #Authenticate
        login_command = f"az login --service-principal --username {client_id} --password {client_secret} --tenant {tenant_id}"
        print(login_command)
        
        returncode, stdout, stderr = run_command(login_command)
        if returncode == 0:
            print("Login Successful")
        else:
            print("Login failed")
            return stderr
        #Run the azure command
        creturncode, cstdout, cstderr = run_command(command=command)
        if creturncode == 0:
            return cstdout
        else:
            return cstderr

        # return jsonify({'stdout': result.stdout, 'stderr': result.stderr})
        # if returncode == 0:
        #     print("Login successful.")
        #     return stdout
        # else:
        #     print("Login failed")
        #     return stdout


# class Callback(Resource):
#     def get(self):
#         code = request.args.get('code')
#         if not code:
#             return {'error': 'Authorization code not provided'}, 400
        
#         token_data = {
#             'grant_type': 'authorization_code',
#             'code': code,
#             'redirect_uri': redirect_uri,
#             'client_id': client_id,
#             'client_secret': client_secret
#         }
#         token_response = requests.post(token_url, data=token_data)
#         token_json = token_response.json()
        
#         if 'access_token' not in token_json:
#             return {'error': 'Failed to retrieve access token'}, 400
        
#         session['access_token'] = token_json['access_token']
#         session['refresh_token'] = token_json['refresh_token']
        
#         return {'message': 'Login successful'}, 200

