from neo4j import GraphDatabase
import time
import Algos.config as config


start = time.time()

# Initialize the Neo4j driver
driver = config.DRIVER

def most_related_category(tx):
    result = tx.run("""
        MATCH (n)<-[r:RELATED_TO]-()
        RETURN n.category AS category, COUNT(r) AS relationship_count
        ORDER BY relationship_count DESC
        LIMIT 1
    """)
    return result.single()

if __name__ == "__main__":
    with driver.session() as session:
        result = session.execute_read(most_related_category)
        runtime = time.time() - start
        print(f"Most related category: {result['category']}")
        print(f"Runtime (seconds): {runtime}\n")

        with open('most_related_category.txt', 'w') as f:
            f.write(f"Most related category: {result['category']} \n")
            f.write(f"Runtime (seconds): {runtime}\n")