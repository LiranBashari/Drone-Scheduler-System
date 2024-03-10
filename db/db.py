from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(mongo_uri)


db = client["WDS-DB"]

# 4 collections
drone_collection = db["Drone-Collection"]
trajectory_collection = db["Trajectory-Collection"]
mission_collection = db["Mission-Collection"]
schedule_collection = db["Schedule-Collection"]