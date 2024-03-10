from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://liranbashari:Liran123!@cluster0.ncbdor0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)


db = client["WDS-DB"]

# 4 collections
drone_collection = db["Drone-Collection"]
trajectory_collection = db["Trajectory-Collection"]
mission_collection = db["Mission-Collection"]
schedule_collection = db["Schedule-Collection"]