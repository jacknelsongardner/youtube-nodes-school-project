from neo4j import GraphDatabase
import time

start = time.time()

# Replace these with your Neo4j credentials
uri = "bolt://localhost:7687"  # Neo4j Bolt protocol address
username = "agunkel"
password = "YoutubeLMAO"

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))



def most_related_uploader(tx):
    result = tx.run("""
        MATCH (n)<-[r:RELATED_TO]-()
        RETURN n.uploader AS uploader, COUNT(r) AS relationship_count
        ORDER BY relationship_count DESC
        LIMIT 1
    """)
    return result.single()

if __name__ == "__main__":
    with driver.session() as session:
        result = session.execute_read(most_related_uploader)
        runtime = time.time() - start
        print(f"Most related uploader: {result['uploader']}")
        print(f"Runtime (seconds): {runtime}\n")

        with open('most_related_uploader.txt', 'w') as f:
            f.write(f"Most related uploader: {result['uploader']} \n")
            f.write(f"Runtime (seconds): {runtime}\n")
