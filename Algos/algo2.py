from neo4j import GraphDatabase
from pyspark.sql import SparkSession
import time
import config
#most common categories algorithm

# Replace these with your Neo4j credentials

# Initialize the Neo4j driver

driver = config.DRIVER
start = time.time()

def get_related(tx):
    query = "MATCH (v:Video) RETURN id(v) AS video, v.category AS cat"
    return list(tx.run(query))

def main():

    with driver.session() as session:
        categories = session.execute_read(get_related)

    spark = SparkSession.builder.appName("vidcategories").getOrCreate()
    data = []
    for video in categories:
        data.append({"videoid" : video["video"], "category" : video["cat"]})

    df = spark.createDataFrame(data) #dataframe containing all related_to relations, with source being source video id and dest being destination id
    df.show()

    rdd = df.rdd
    rdd = rdd.flatMap(lambda row: [(cat, 1) for cat in row['category']]) #map, (category, 1), have to do the python list thing because category is a list
    cat_sum = rdd.reduceByKey(lambda x, y: x + y) #reduce
    result = cat_sum.toDF(["category", "count"])
    result = result.orderBy(result['count'].desc())
    result.show()

    runtime = time.time() - start

    top_30 = result.head(30)

    with open('top_30_categories.txt', 'w') as f:
        f.write(f"Runtime (seconds): {runtime}\n")
        for item in top_30:
            f.write(f"{item}\n")

if __name__ == "__main__":
    main()
