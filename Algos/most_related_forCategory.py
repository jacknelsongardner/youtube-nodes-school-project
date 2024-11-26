from neo4j import GraphDatabase
import time
import config

start = time.time()

# Initialize the Neo4j driver
driver = config.DRIVER

def most_related_video_for_category(tx, category):
    result = tx.run("""
        MATCH (n)-[:RELATED_TO]->(m)
        WHERE n.category = $category
        RETURN id(n) AS video_id, COUNT(*) AS relationship_count
        ORDER BY relationship_count DESC
        LIMIT 1
    """, category=category)
    return result.single()

def ui_run(category=["Music"]):
    with driver.session() as session:
        #Can use input to input custom IDs this was for test
        result = session.execute_read(most_related_video_for_category, category)
        runtime = time.time() - start
        print(f"Most related video for category: {category} is {result['video_id']}")
        print(f"Runtime (seconds): {runtime}\n")


        with open('most_related_video_for_category.txt', 'w') as f:
            f.write(f"Most related video for category: {category} is {result['video_id']}\n")
            f.write(f"Runtime (seconds): {runtime}\n")

    return result['video_id']

if __name__ == "__main__":
    ui_run()
