import subprocess
import json

def login_with_service_principal(client_id, client_secret, tenant_id):
    try:
        # Log in to Azure using the service principal credentials
        login_command = [
            'az', 'login',
            '--service-principal',
            '--username', client_id,
            '--password', client_secret,
            '--tenant', tenant_id
        ]
        result = subprocess.run(login_command, check=True, capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}

def run_azure_command(command):
    try:
        # Run the specified Azure CLI command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return {"status": "success", "output": json.loads(result.stdout)}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
