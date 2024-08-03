import subprocess
from flask import jsonify, make_response, render_template, request
from flask_restful import Resource
from flask_login import login_required
from resources.azure_cli import login_with_service_principal, run_azure_command

def run_command(command):
    if isinstance(command, str):
        command = command.split()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')

class AuthAzure(Resource):
    @login_required
    def get(self):
        return make_response(render_template("credentials.html"))
    
    @login_required
    def post(self):
        pass
    

class RunCommand(Resource):
    @login_required
    def post(self):
        data = request.json

        client_id = data.get("clientId")
        client_secret = data.get("clientSecret")
        tenant_id = data.get("tenantId")
        command = data.get("command")

        # Login using service principal
        if login_with_service_principal(client_id, client_secret, tenant_id):
            # Run the specified Azure CLI command
            command_response = run_azure_command(command.split())
            print(command_response)
            return jsonify({"result":command_response})
        else:
            return jsonify({"error":"Failed to log in"}), 400
        

class AzureCliResponse(Resource):
    @login_required
    def get(self):
        return make_response(render_template("result_page.html"))