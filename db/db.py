from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(mongo_uri)

db = client["WDS-DB"]

# Define collections
drone_collection = db["Drone-Collection"]
trajectory_collection = db["Trajectory-Collection"]
mission_collection = db["Mission-Collection"]
schedule_collection = db["Schedule-Collection"]

# Create indexes
drone_collection.create_index("_id")
drone_collection.create_index("current_mission_id")
drone_collection.create_index("possible_mission_ids")

schedule_collection.create_index("drone_id")
schedule_collection.create_index("mission_id")

mission_collection.create_index("_id")
mission_collection.create_index("trajectory_id")
