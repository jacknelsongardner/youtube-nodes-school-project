from neo4j import GraphDatabase
from pyspark.sql import SparkSession
import time

#the third algorithm, this gets the most commonly related categories, at search_depth


# Replace these with your Neo4j credentials
uri = "bolt://localhost:7687"  # Neo4j Bolt protocol address
username = "kai"
password = "abcd1234"
SEARCH_DEPTH = 2
# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_related(tx):
    query = f"MATCH (src:Video)-[:RELATED_TO*1..{SEARCH_DEPTH}]->(rec:Video) RETURN src.category AS sourcecat, rec.category AS reccat"
    return list(tx.run(query))


if __name__ == "__main__":

    with driver.session() as session:
        relateds = session.execute_read(get_related)

    start = time.time()

    spark = SparkSession.builder.appName("catrelations2bydepth").getOrCreate()
    data = []
    for relation in relateds:
        source_cat = relation["sourcecat"]
        rec_cat = relation["reccat"]
        #if the categories are lists, convert them to strings to prevent spark from blowing up when performing the map reduce
        if isinstance(source_cat, list):
            source_cat = ",".join(source_cat)
        if isinstance(rec_cat, list):
            rec_cat = ",".join(rec_cat)
        data.append({"source" : source_cat, "rec" : rec_cat})

    df = spark.createDataFrame(data) #dataframe containing all relations, with source being source categories and rec being recommended category list
    df.show()


    rdd = df.rdd
    rdd = rdd.map(lambda row: ((row['source'], row['rec']), 1))
    relation_sum = rdd.reduceByKey(lambda x, y: x + y) #reduce
    result = relation_sum.toDF(["categories", "num_relations"])
    result = result.orderBy(result['num_relations'].desc())
    result.show()


    runtime = time.time() - start

    top_30 = result.head(30)
    with open(f'top_30_category_to_category_{SEARCH_DEPTH}.txt', 'w') as f:
        f.write(f"Search Depth: {SEARCH_DEPTH}, Runtime (seconds): {runtime}\n")
        for item in top_30:
            f.write(f"{item}\n")
