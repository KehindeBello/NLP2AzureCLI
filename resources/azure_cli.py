import subprocess
from dotenv import load_dotenv
import os

# Function to run a subprocess command
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')

load_dotenv()
# Service Principal credentials
client_id = os.getenv("client_id")
client_secret = os.getenv("client_Secret")
tenant_id = os.getenv("tenant_id")

# Login using Service Principal
login_command = f"az login --service-principal --username {client_id} --password {client_secret} --tenant {tenant_id}"
returncode, stdout, stderr = run_command(login_command)

if returncode == 0:
    print("Login successful.")
    print(stdout)
    
    # Run your Azure CLI command
    az_command = "az group list"
    returncode, stdout, stderr = run_command(az_command)
    
    if returncode == 0:
        print("Command executed successfully.")
        print(stdout)
    else:
        print("Command execution failed.")
        print(stderr)
else:
    print("Login failed.")
    print(stderr)
