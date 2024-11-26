from neo4j import GraphDatabase
from datetime import datetime

# Get the current time
start = datetime.now()

import config

# Initialize the Neo4j driver
driver = config.DRIVER

def connect_to_neo4j(uri, username, password):
    """
    Establishes a connection to the Neo4j database.
    """
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver

def query_node_and_relations( video_id="LKh7zAJ4nwo"):
    """
    Queries a specific node by video_id and retrieves all relationships and attributes of the node.
    """
    with driver.session() as session:
        query = """
        MATCH (n {id: $video_id})
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN n, r, m
        """
        result = session.run(query, video_id=video_id)
        
        for record in result:
            node = record["n"]
            relation = record["r"]
            related_node = record["m"]
            
            # Print node properties
            if node:
                print("Node Properties:")
                for key, value in node.items():
                    print(f"  {key}: {value}")
            
            # Print relationships
            if relation:
                print("\nRelationships:")
                print(f"  Relationship: {relation.type}")
                if related_node:
                    print(f"  Related Node ID: {related_node.id} - Node Properties:")
                    for key, value in related_node.items():
                        print(f"    {key}: {value}")
                else:
                    print("  No related node for this relationship.")
            else:
                print("\nNo relationships found.")
            
            print("-" * 40)

def close_neo4j_connection(driver=driver):
    """
    Closes the connection to the Neo4j database.
    """
    driver.close()

def ui_run(video_id):
    # Query the node and its relations
    query_node_and_relations(video_id)

    # Close the connection
    close_neo4j_connection(driver)


    end = datetime.now()

    print(start)
    print(end)
    print(end - start)

if __name__ == "__main__":

    video_id = "LKh7zAJ4nwo"  # Replace with your specific video_id

    ui_run(video_id=video_id)



