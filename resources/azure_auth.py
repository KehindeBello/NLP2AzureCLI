import subprocess
import uuid
from flask import Response, jsonify, make_response, redirect, render_template, request, session, stream_with_context, url_for
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
        #store the from data in the session
        print('I am here in post credentials')
        data = request.json
        session['client_id'] = data.get('clientId')
        session["client_secret"] = data.get("clientSecret")
        session["tenant_id"] = data.get("tenantId")
        session["command"] = data.get("command")

        #redirect to the output page with a reference
        print('i have set session data')
        return make_response(render_template('result_page.html'))
    

class RunCommand(Resource):
    @login_required
    def post(self):
        # data = request.json

        client_id = session.get("client_id")
        client_secret = session.get("client_secret")
        tenant_id = session.get("tenant_id")
        command = session.get("command")

        print(f"Command: {command}")
        # Login using service principal
        if login_with_service_principal(client_id, client_secret, tenant_id):
            # Run the specified Azure CLI command
            def generate():
                process = subprocess.Popen(command.split(), 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.STDOUT)
                for line in iter(process.stdout.readline, b''):
                    yield line.decode('utf-8')
                process.stdout.close()
                process.wait()

            return Response(stream_with_context(generate()), mimetype='text/plain')
        
        else:
            return jsonify({"error": "Failed to log in"}), 400
        

class AzureCliResponse(Resource):
    @login_required
    def get(self):
        return make_response(render_template("result_page.html"))