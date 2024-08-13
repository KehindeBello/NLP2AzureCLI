import json
import re
import spacy
from spacy.tokens import Doc
from spacy.training import Example
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline



# Function to load the JSON resource file
def load_resources(file_path):
    """
    Load the Azure CLI resources from a JSON file.

    :param file_path: Path to the JSON file containing Azure CLI resources
    :return: Dictionary containing the loaded resources
    """
    file_path = "resources/ner_trial/azure_cli_resources.json"
    with open(file_path, "r") as file:
        return json.load(file)


# Function to prepare training data for the intent classification model
def prepare_training_data(resources):
    """
    Prepare training data for the intent classification model.

    :param resources: Dictionary containing Azure CLI resources
    :return: X (list of input patterns), y (list of corresponding intents)
    """
    X = []  # List to store input patterns
    y = []  # List to store corresponding intents
    for intent, data in resources.items():
        for pattern in data["patterns"]:
            X.append(pattern)
            y.append(intent)
    return X, y


# Function to train the intent classification model
def train_model(X, y):
    """
    Train the intent classification model using scikit-learn.

    :param X: List of input patterns
    :param y: List of corresponding intents
    :return: Trained scikit-learn Pipeline object
    """
    with open('resources/ner_trial/intent_data.json', 'r') as file:
        data = json.load(file)

    # Extract X (input patterns) and y (intents)
    X = [item['input'] for item in data['data']]
    y = [item['intent'] for item in data['data']]
    # Create a pipeline with CountVectorizer and MultinomialNB
    model = Pipeline(
        [
            ("vectorizer", CountVectorizer()),  # Convert text to vector of token counts
            (
                "classifier",
                MultinomialNB(),
            ),  # Naive Bayes classifier for multinomial models
        ]
    )
    model.fit(X, y)  # Train the model
    return model


# Function to preprocess user input
def preprocess(text):
    """
    Preprocess the user input by converting to lowercase and removing punctuation.

    :param text: User input text
    :return: Preprocessed text
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text


# Function to extract parameters from user input
def extract_params(user_input, param_patterns, nlp):
    """
    Extract parameters from user input using regex patterns and custom spaCy NER.

    :param user_input: User input text
    :param param_patterns: Dictionary of parameter regex patterns
    :param nlp: spaCy NLP object
    :return: Dictionary of extracted parameters
    """
    params = {}
    doc = nlp(user_input)  # Process the user input with spaCy

    for param, pattern in param_patterns.items():
        print(f"Param, Pattern -- {param}, {pattern}")
        for ent in doc.ents:
            print(ent)
            if ent.label_ == param.upper():
                params[param] = ent.text
                print(f"Paramas after entitty - {params}")
                break
    print(f"Params to go {params}")
    return params


# Function to generate Azure CLI command
def generate_azure_cli_command(intent, params, resources):
    """
    Generate Azure CLI command based on intent and parameters.

    :param intent: Detected intent
    :param params: Dictionary of extracted parameters
    :param resources: Dictionary containing Azure CLI resources
    :return: Generated Azure CLI command
    :raises ValueError: If required parameters are missing
    """
    command_template = resources[intent]["command"]
    # Find all required parameters in the command template
    required_params = set(re.findall(r"\{(\w+)\}", command_template))
    # Identify missing parameters
    missing_params = required_params - set(params.keys())

    if missing_params:
        raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

    # Replace placeholders in the command template with actual parameter values
    # print(f"")
    for param, value in params.items():
        placeholder = "{" + param + "}"
        command_template = command_template.replace(placeholder, value)

    return command_template


# Function to suggest missing parameters to the user
def suggest_missing_params(missing_params, resources, intent):
    """
    Generate suggestions for missing parameters.

    :param missing_params: Set of missing parameter names
    :param resources: Dictionary containing Azure CLI resources
    :param intent: Detected intent
    :return: List of parameter suggestions with descriptions
    """
    suggestions = []
    for param in missing_params:
        if (
            "param_description" in resources[intent]
            and param in resources[intent]["param_description"]
        ):
            suggestions.append(
                f"{param}: {resources[intent]['param_description'][param]}"
            )
        else:
            suggestions.append(param)
    return suggestions


# Main function
def ner_to_command(prompt):
    """
    Main function to run the Azure CLI Command Generator.
    """
    resource_file = "azure_cli_resources.json"  # Path to the JSON resource file
    resources = load_resources(resource_file)

    # Prepare training data and train the model
    X, y = prepare_training_data(resources)
    model = train_model(X, y)

    # Load spaCy model
    nlp = spacy.load("resources/ner_trial/path_to_saved_model_sharp")

    # Add custom NER labels based on parameters in the resource file
    ner = nlp.get_pipe("ner")
    for intent in resources:
        for param in resources[intent]["param_patterns"]:
            if param.upper() not in ner.labels:
                ner.add_label(param.upper())

    # Train the NER model with an empty example to initialize the new labels
    optimizer = nlp.create_optimizer()
    for _ in range(10):  # Adjust the number of iterations as needed
        losses = {}
        doc = Doc(nlp.vocab, words=["Example", "sentence", "for", "custom", "NER", "training"])
        example = Example.from_dict(doc, {"entities": []})
        nlp.update([example], sgd=optimizer, losses=losses)

    print("Advanced Azure CLI Command Generator: Hello! Type 'quit' to exit.")
    while True:
        user_input = prompt
        if user_input.lower() == "quit":
            print("Advanced Azure CLI Command Generator: Goodbye!")
            break

        processed_input = preprocess(user_input)
        intent = model.predict([processed_input])[0]  # Predict the intent
        print(f"Intent, {intent}")

        if intent in resources:
            try:
                # Extract parameters and generate command
                params = extract_params(
                    user_input, resources[intent]["param_patterns"], nlp
                )
                print(f"Params, {params}")
                command = generate_azure_cli_command(intent, params, resources)
                print("Azure CLI Command:")
                return command
            except ValueError as e:
                # Handle missing parameters
                print(f"Error: {str(e)}")
                missing_params = set(
                    re.findall(r"\{(\w+)\}", resources[intent]["command"])
                ) - set(params.keys())
                suggestions = suggest_missing_params(missing_params, resources, intent)
                print("Please provide the following parameters:")
                for suggestion in suggestions:
                    # print(f"- {suggestion}")
                    return f"- {suggestion}"
        else:
            return "I'm not sure how to generate that Azure CLI command. Can you please try rephrasing your request?"
