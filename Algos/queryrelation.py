from neo4j import GraphDatabase

import config

driver = config.DRIVER

def connect_to_neo4j(uri, username, password):
    """
    Establishes a connection to the Neo4j database.
    """
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver

def get_all_relationships( node_value):
    """
    Queries all relationships for a node by its ID and prints related node IDs.
    """
    with driver.session() as session:
        # Query to get relationships from a node with a specific id
        query = """
        MATCH (n {id: $node_value})
        OPTIONAL MATCH (n)-[r]->(m)
        OPTIONAL MATCH (n)<-[r_in]-(m_in)
        RETURN n, r, m, r_in, m_in
        """
        
        # Run the query and pass the node_value as a parameter
        result = session.run(query, node_value=node_value)
        
        relationships_found = False
        
        # Debug: Ensure we are receiving results
        print(f"Querying for node with ID: {node_value}")
        
        # Iterate through the result
        for record in result:
            # Get the related nodes from the record
            related_node = record["m"]
            related_node_in = record["m_in"]
            
            # Check if there are any related nodes and print their IDs
            if related_node:
                print(f"Related Node ID (Outgoing): {related_node.id}")
                relationships_found = True
                
            if related_node_in:
                print(f"Related Node ID (Incoming): {related_node_in.id}")
                relationships_found = True
        
        # If no relationships were found
        if not relationships_found:
            print("No relationships found for this node.")

def close_neo4j_connection():
    """
    Closes the connection to the Neo4j database.
    """
    driver.close()

if __name__ == "__main__":
    node_value = "OM_Rx-5UYuw"  # Replace with the specific node ID

    # Get all relationships for the node and print related node IDs
    get_all_relationships(node_value)

    # Close the connection
    close_neo4j_connection(driver)
