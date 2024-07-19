from flask_jwt_extended import jwt_required
from resources.nlp_to_command import translate_to_azure_cli
from flask import jsonify, request
from flask_restful import Resource

class ConvertNLP(Resource):
    def post(self):
        data = request.json
        nlp_input = data.get('nlpInput')
        print(nlp_input)
        # Logic to convert NLP to Azure CLI command
        azure_cli_command = translate_to_azure_cli(nlp_input)
        print(azure_cli_command)
        return jsonify({'azureCliCommand': azure_cli_command})
