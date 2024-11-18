from neo4j import GraphDatabase

# Replace these with your Neo4j credentials
uri = "bolt://localhost:7687"  # Neo4j Bolt protocol address
username = "jack"
password = "Xfiles12345!!!!!"

# Initialize the Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))





# Open the file and read the content
def parse_file(file_path):
    with open(file_path, 'r') as file:
        # Read the file content and split by tab/newline characters
        data = file.read()
    splitByLine = data.split("\n")
    
    output = []

    for line in splitByLine:
        
        splitBySpace = line.split()
        #print(splitBySpace)
        output.append(splitBySpace)

    return output

#print(data_list)
def get_nodes(list):
    
    output = {}
    for l in list:
        # The first item is the initial video ID and title, we assume the format [ID Title]
        try:
            main_video_id = l[0]
            output[main_video_id] = 'node'
        except:
            pass

        
    return output


def get_cypher_node(list):
    
    # The first item is the initial video ID and title, we assume the format [ID Title]
    main_video_id = list[0]
    main_video_creator = list[1]
    age = ""
    cat = ""
    length = ""
    views = ""
    rate = ""
    ratings = ""
    comments = ""
    related_video_ids = []

    if list[4] == "&":
        age = list[2]
        cat = f"['{list[3]}', '{list[5]}']"
        length = list[6]
        views = list[7]
        rate = list[8]
        ratings = list[9]
        comments = list[10]

        # The rest of the data consists of video IDs (assume they are related)
        related_video_ids = list[11:]
    
    else:
        age = list[2]
        cat = f"['{list[3]}']"
        length = list[4]
        views = list[5]
        rate = list[6]
        ratings = list[7]
        comments = list[8]
    
        # The rest of the data consists of video IDs (assume they are related)
        related_video_ids = list[9:]



    # Generate Cypher statements
    #cypher_statements = []
      
    # for the node whose entry we find in 0.txt
    newNode = "CREATE (main:Video {id: '" + main_video_id + "', uploader: '" + main_video_creator + "', age: " + age + ", category:" + cat+ ", length:" + length+", views:"+ views +", rate:" + rate +", ratings:" + ratings+", comments:" + comments +"});"
    print(newNode)
    return newNode

def get_cypher_nodes(list):
    output = []
    for item in list:
        try:
            output.append(get_cypher_node(item))
        except Exception as e:
            print(e)
    return output


def get_cypher_relations(list, nodes: dict):
    cypher_output = []
    
    for elem in list:
        try:
            main_video_id = elem[0]
            
            # The rest of the data consists of video IDs (assume they are related)
            related_video_ids = elem[9:]

            # Generate relationships if related video IDs exist in nodes
            for related_id in related_video_ids:
                if related_id in nodes.keys():
                    # Create the Cypher relationship statement
                    relation_statement = f"""
                    MATCH (main:Video {{id: '{main_video_id}'}})
                    MATCH (related:Video {{id: '{related_id}'}})
                    CREATE (main)-[:RELATED_TO]->(related);
                    """
                    cypher_output.append(relation_statement.strip())
        except: 
            pass

    return cypher_output



# Output Cypher to a file for execution in Neo4j
def output_cypher(cypher_statements, output_path):
    with open(output_path, 'w') as output_file:
        for statement in cypher_statements:
            output_file.write(statement + '\n')

# Function to execute a list of Cypher commands
def execute_cypher_commands(commands):
    with driver.session() as session:
        for command in commands:
            try:
                # Run each Cypher command
                session.run(command)
                print(f"Executed: {command}")
            except Exception as e:
                print(f"Error executing command: {command}")
                print(e)

print("deleting contents before parsing...please wait")
execute_cypher_commands(["MATCH (n) DETACH DELETE n"])

i = 0
while True:
    try:
        data_list = parse_file(f"{i}.txt")

        nodeIDs = get_nodes(data_list)

        nodeCypher = get_cypher_nodes(data_list)

        relationCypher = get_cypher_relations(data_list, nodeIDs)

        commands = nodeCypher + ["\n"] + relationCypher

        output_cypher(commands, f"{i}.cypher")
        print(f"saved cypher commands for layer {i}")
        execute_cypher_commands(commands)
        print(f"executed cypher commands for {i}")

        i = i + 1
    except:
        print(f"no file found for {i}.txt, stopping with {i-1} cypher outputs")

print("Cypher commands written")