from time import sleep
from datetime import datetime
from db.db import schedule_collection, drone_collection
from dotenv import load_dotenv
import os

load_dotenv()
thread_interval = int(os.getenv("THREAD_INTERVAL"))


def mission_firing_thread():
    while True:
        current_datetime = datetime.utcnow()
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")

        missions_to_start = schedule_collection.find({"start_time": {"$lte": formatted_datetime}, "status": "scheduled"})
        for mission in missions_to_start:
            # Update drone status to "on a mission"
            drone_collection.update_one({"_id": mission["drone_id"]}, {"$set": {"status": "on-mission"}})
            # Update mission status to "in progress"
            schedule_collection.update_one({"_id": mission["_id"]}, {"$set": {"status": "in-progress"}})

        # Check for missions that have ended and update statuses
        missions_to_complete = schedule_collection.find({"end_time": {"$lte": formatted_datetime}, "status": "in-progress"})
        for mission in missions_to_complete:
            # Update drone status to "available"
            drone_collection.update_one({"_id": mission["drone_id"]}, {"$set": {"status": "available"}})

            # Update mission status to "completed"
            schedule_collection.update_one({"_id": mission["_id"]}, {"$set": {"status": "completed"}})
        
        sleep(thread_interval)
