from neo4j import GraphDatabase
import time
uri = "bolt://localhost:7687"  # Neo4j Bolt protocol address
username = "jack"
password = "Xfiles12345!!!!!"

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

def getKey(val):
    return val[1]

def reduceIt(cats):
    results = []
    for cat in cats:
        total = 0
        query = "match (n) where '" + str(cat) + "' in n.category return n.views order by n.views desc"
        myRecords, summary, keys = driver.execute_query(query)
        for item in myRecords:
            views = int(item.values()[0])
            total = total + int(views)
        results.append((cat, total))
    return sorted(results, key=getKey, reverse= True)

def topXVideos(myAmount):
    query = "match (n) return n.title, n.views order by n.views desc limit " + str(myAmount)
    records, summary, keys = driver.execute_query(query)
    output = ''
    for item in records:
        output = output + ", " + str(item)
    return output

def topXViewedInCat(myAmount, myCategory):
    query = "match (n) where '" + myCategory + "' in n.category return n.title, n.views order by n.views desc limit " + str(myAmount)
    records, summary, keys = driver.execute_query(query)
    output = ''
    for item in records:
        output = output + ", " + str(item)
    return output

def topXViewedCats(myAmount):
    query = "MATCH (n) WHERE n.category is not null RETURN DISTINCT n.category AS category"
    records, summary, keys = driver.execute_query(query)
    categoriesFound = []
    for item in records:
        values = item.values()
        for value in values:
            for val in value:
                categoriesFound.append(val)
    orderedCats = reduceIt(categoriesFound)
    return str(orderedCats[:int(myAmount)])


# def main():
#     while True:
#         myInput = int(input("would you like to (1) see the top x viewed videos, (2) see the top x viewed videos in a category, (3) see the top x viewed categories, or (4) quit?"))
#         myAmount = (input("how many?"))
#         start = time.time()
#         if myInput == 1:
#             print("finding top videos...")
#             query = "match (n) return n.title, n.views order by n.views desc limit " + str(myAmount)
#             records, summary, keys = driver.execute_query(query)
#             for item in records:
#                 print(item)
#         elif myInput == 2:
#             whatCat = input("what category?")
#             print("finding top videos in " + str(whatCat))
#             query = "match (n) where '" + whatCat + "' in n.category return n.title, n.views order by n.views desc limit " + str(myAmount)
#             records, summary, keys = driver.execute_query(query)
#             for item in records:
#                 print(item)
#         elif myInput == 3:
#             print("finding top viewed categories")
#             query = "MATCH (n) WHERE n.category is not null RETURN DISTINCT n.category AS category"
#             records, summary, keys = driver.execute_query(query)
#             categoriesFound = []
#             for item in records:
#                 values = item.values()
#                 for value in values:
#                     for val in value:
#                         categoriesFound.append(val)
#             orderedCats = reduceIt(categoriesFound)
#             print(orderedCats[:int(myAmount)])
#         else:
#             print("exiting")
#             break
#         end = time.time()
#         print(str(end-start))

def main():
    1=1

if __name__ == "__main__":
    main()