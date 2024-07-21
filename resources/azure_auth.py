import subprocess
from flask import jsonify, make_response, render_template, request
from flask_restful import Resource
from flask_login import login_required

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

        print(type(command))
        print(f'Clientid - {client_id}, Clientsecret - {client_secret}, TenantId - {tenant_id}, Command - {command}')
        #Authenticate
        login_command = f"az login --service-principal --username {client_id} --password {client_secret} --tenant {tenant_id}"
        print(login_command)
        try:
            returncode, stdout, stderr = run_command(login_command)
            if returncode == 0:
                print("Login Successful")
                # Ensure the command is a list of strings if not already
                if isinstance(command, str):
                    command = command.split()

                print(f'Executing Azure CLI command: {command}')
                creturncode, cstdout, cstderr = run_command(command)

                if creturncode == 0:
                    return jsonify({"output": cstdout})
                else:
                    return jsonify({"error": cstderr}), 400
            else:
                print("Login failed")
                return jsonify({"error": stderr}), 400
        except:
            return jsonify({'error': "Error"})