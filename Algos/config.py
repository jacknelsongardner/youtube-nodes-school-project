import json
from neo4j import GraphDatabase

# Path to the JSON file
json_file_path = 'config.json'

# Read and parse the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract elements and sethem to string variables
USERNAME = str(data.get("username", ""))
URI = str(data.get("uri", ""))
PASSKEY = str(data.get("password", ""))

# Print the variables
print("LOGGING IN WITH :")
print(f"Name: {USERNAME}")
print(f"URI: {URI}")

# Initialize the Neo4j driver
DRIVER = GraphDatabase.driver(URI, auth=(USERNAME, PASSKEY))
