from neo4j import GraphDatabase
from pyspark.sql import SparkSession
import time
import config
#the third algorithm, this gets the most recommended categories, searching at
#the parameter SEARCH_DEPTH depth.


# Replace these with your Neo4j credentials
SEARCH_DEPTH = 2
# Initialize the Neo4j driver

driver = config.DRIVER

def get_related(tx):
    query = f"MATCH (src:Video)-[:RELATED_TO*1..{SEARCH_DEPTH}]->(rec:Video) RETURN src.id AS source, rec.category AS categories"
    return list(tx.run(query))

start = time.time()

if __name__ == "__main__":
    with driver.session() as session:
        relateds = session.execute_read(get_related)

    spark = SparkSession.builder.appName("catrelationsbydepth").getOrCreate()
    data = []
    for relation in relateds:
        data.append({"source" : relation["source"], "category" : relation["categories"]})

    df = spark.createDataFrame(data) #dataframe containing all related_to relations, with source being source video id and category being category list
    df.show()


    rdd = df.rdd
    rdd = rdd.flatMap(lambda row: [(cat, 1) for cat in row['category']]) #map, (category, 1), have to do the python list thing because category is a list
    relation_sum = rdd.reduceByKey(lambda x, y: x + y) #reduce
    result = relation_sum.toDF(["category", "num_relations"])
    result = result.orderBy(result['num_relations'].desc())
    result.show()


    runtime = time.time() - start

    top_30 = result.head(30)
    with open(f'top_30_recommended_categories_{SEARCH_DEPTH}.txt', 'w') as f:
        f.write(f"Search Depth: {SEARCH_DEPTH}, Runtime (seconds): {runtime}\n")
        for item in top_30:
            f.write(f"{item}\n")
