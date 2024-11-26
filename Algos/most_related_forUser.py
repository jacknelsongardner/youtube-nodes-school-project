from neo4j import GraphDatabase
import time
import config

start = time.time()

# Initialize the Neo4j driver
driver = config.DRIVER

def most_related_video_for_user(tx, user_id):
    result = tx.run("""
        MATCH (n)-[:RELATED_TO]->(m)
        WHERE n.title = $user_id
        RETURN id(n) AS video_id, COUNT(*) AS relationship_count
        ORDER BY relationship_count DESC
        LIMIT 1
    """, user_id=user_id)
    return result.single()

def ui_run(user_id="JiveRecords"):
    with driver.session() as session:
        #Can use input to input custom IDs this was for test
        result = session.execute_read(most_related_video_for_user, user_id)
        runtime = time.time() - start
        print(f"Most related video for user: {user_id} is {result['video_id']}")
        print(f"Runtime (seconds): {runtime}\n")


        with open('most_related_video_for_user.txt', 'w') as f:
            f.write(f"Most related video for user: {user_id} is {result['video_id']}\n")
            f.write(f"Runtime (seconds): {runtime}\n")

    return result['video_id']

if __name__ == "__main__":
    ui_run()
