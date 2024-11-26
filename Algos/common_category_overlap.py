from neo4j import GraphDatabase
import time
import config

start = time.time()

driver = config.DRIVER

def find_categories_with_highest_shared_recommendations(tx):
    result = tx.run("""
        MATCH (n)-[:RELATED_TO]->(a), (n)-[:RELATED_TO]->(b)
        WHERE a.category <> b.category
        WITH a.category AS category_a, b.category AS category_b, COUNT(n) AS shared_nodes
        RETURN category_a, category_b, shared_nodes
        ORDER BY shared_nodes DESC
        LIMIT 1
    """)
    return result.single()


if __name__ == "__main__":
def ui_run():
    with driver.session() as session:
        result = session.execute_read(find_categories_with_highest_shared_recommendations)
        runtime = time.time() - start
        print(f"The two categories recommended together most often are: {result['category_a']} and {result['category_b']}")
        print(f"Runtime (seconds): {runtime}\n")

        with open('most_mutually_related_categories.txt', 'w') as f:
            f.write(f"The two categories recommended together most often are: {result['category_a']} and {result['category_b']} \n")
            f.write(f"Runtime (seconds): {runtime}\n")

    return result['category_a'], result['category_b']