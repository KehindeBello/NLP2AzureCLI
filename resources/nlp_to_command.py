import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.llms import openai
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set up the OpenAI API key. Load environmental variables
load_dotenv()

# Initialize the OpenAI LLM
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define a prompt template for generating Azure CLI commands
prompt_template = """
Translate the following natural language instruction into an Azure CLI command:

Instruction: {instruction}

Azure CLI Command:
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["instruction"])

# Create the LangChain with the LLM and the prompt template
chain = LLMChain(prompt=prompt, llm=llm)

# Define a function to translate instructions to Azure CLI commands
def translate_to_azure_cli(instruction):
    azure_cli_command = chain.run(instruction)
    return azure_cli_command

# Example usage
# instruction = "Get a list of resource groups."
# azure_cli_command = translate_to_azure_cli(instruction)
# print("Azure CLI Command:", azure_cli_command)
