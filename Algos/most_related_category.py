from neo4j import GraphDatabase
import time

start = time.time()

# Replace these with your Neo4j credentials
uri = "bolt://localhost:7687"  # Neo4j Bolt protocol address
username = "agunkel"
password = "YoutubeLMAO"

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))


def most_related_category(tx):
    result = tx.run("""
        MATCH (n)<-[r:RELATED_TO]-()
        RETURN n.category AS category, COUNT(r) AS relationship_count
        ORDER BY relationship_count DESC
        LIMIT 1
    """)
    return result.single()

with driver.session() as session:
    result = session.execute_read(most_related_category)
    runtime = time.time() - start
    print(f"Most related category: {result['category']}")
    print(f"Runtime (seconds): {runtime}\n")

    with open('most_related_category.txt', 'w') as f:
        f.write(f"Most related category: {result['category']} \n")
        f.write(f"Runtime (seconds): {runtime}\n")