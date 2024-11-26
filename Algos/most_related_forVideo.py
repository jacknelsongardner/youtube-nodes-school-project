from neo4j import GraphDatabase
import time
import Algos.config as config



start = time.time()


# Initialize the Neo4j driver
driver = config.DRIVER



def most_related_category_for_vid(tx, node_id):
    result = tx.run("""
        MATCH (n)-[:RELATED_TO]->(m)
        WHERE n.id = $node_id
        RETURN m.category AS category, COUNT(*) AS relationship_count
        ORDER BY relationship_count DESC
        LIMIT 1
    """, node_id=node_id)
    return result.single()


if __name__ == "__main__":

    with driver.session() as session:
        node_id = "ztIH6tc6Aa4" #Can use input to input custom IDs this was for test
        result = session.execute_read(most_related_category_for_vid, node_id)
        runtime = time.time() - start
        print(f"Most related category for video: {node_id} is {result['category']}")
        print(f"Runtime (seconds): {runtime}\n")

def ui_run(node_id="ztIH6tc6Aa4"):
    with driver.session() as session:
        #Can use input to input custom IDs this was for test
        result = session.execute_read(most_related_category_for_vid, node_id)
        runtime = time.time() - start
        print(f"Most related category for video: {node_id} is {result['category']}")
        print(f"Runtime (seconds): {runtime}\n")

        with open('most_related_category_for_vid.txt', 'w') as f:
            f.write(f"Most related category for video: {node_id} is {result['category']}\n")
            f.write(f"Runtime (seconds): {runtime}\n")

=======
    return result['category']
