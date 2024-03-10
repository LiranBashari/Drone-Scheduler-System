from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://liranbashari:Liran123!@cluster0.ncbdor0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

data_base = client["WDS DB"]