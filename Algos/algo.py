from neo4j import GraphDatabase
from pyspark.sql import SparkSession
import time
import config
#The first algorithm, this just counts the videoids that are most recommended


# Replace these with your Neo4j credentials

# Initialize the Neo4j driver

driver = config.DRIVER

start = time.time()

def get_related(tx):
    query = "MATCH (v1:Video)-[:RELATED_TO]->(v2:Video) RETURN id(v1) AS source, id(v2) AS dest"
    return list(tx.run(query))


def main():
    with driver.session() as session:
        relateds = session.execute_read(get_related)

    spark = SparkSession.builder.appName("vidrelations").getOrCreate()
    data = []
    for relation in relateds:
        data.append({"source" : relation["source"], "dest" : relation["dest"]})

    df = spark.createDataFrame(data) #dataframe containing all related_to relations, with source being source video id and dest being destination id
    df.show()


    rdd = df.rdd
    rdd = rdd.flatMap(lambda row: [(row['dest'], 1)]) #map, (video, 1)
    relation_sum = rdd.reduceByKey(lambda x, y: x + y) #reduce
    result = relation_sum.toDF(["video", "num_relations"])
    result = result.orderBy(result['num_relations'].desc())
    result.show()

    runtime = time.time() - start

    top_30 = result.head(30)
    with open('top_30_videos.txt', 'w') as f:
        f.write(f"Runtime (seconds): {runtime}\n")
        for item in top_30:
            f.write(f"{item}\n")


if __name__ == "__main__":
    main()