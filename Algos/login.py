import json
from neo4j import GraphDatabase

# Path to the JSON file
json_file_path = 'login.json'

# Read and parse the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extract elements and set them to string variables
USERNAME = str(data.get("username", ""))
URI = str(data.get("uri", ""))
PASSKEY = str(data.get("password", ""))

# Print the variables
print("LOGGING IN WITH :")
print(f"Name: {USERNAME}")
print(f"City: {URI}")

# Replace these with your Neo4j credentials
uri = "bolt://localhost:7687"  # Neo4j Bolt protocol address
username = "agunkel"
password = "YoutubeLMAO"

# Initialize the Neo4j driver
DRIVER = GraphDatabase.driver(uri, auth=(username, password))