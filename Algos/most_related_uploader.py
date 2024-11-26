from neo4j import GraphDatabase
import time
import Algos.config as config

start = time.time()


# Initialize the Neo4j driver
driver = config.DRIVER



def most_related_uploader(tx):
    result = tx.run("""
        MATCH (n)<-[r:RELATED_TO]-()
        RETURN n.uploader AS uploader, COUNT(r) AS relationship_count
        ORDER BY relationship_count DESC
        LIMIT 1
    """)
    return result.single()


def ui_run():
    with driver.session() as session:
        result = session.execute_read(most_related_uploader)
        runtime = time.time() - start
        print(f"Most related uploader: {result['uploader']}")
        print(f"Runtime (seconds): {runtime}\n")

        with open('most_related_uploader.txt', 'w') as f:
            f.write(f"Most related uploader: {result['uploader']} \n")
            f.write(f"Runtime (seconds): {runtime}\n")

    return result['uploader']

if __name__ == "__main__":
    ui_run()
