from time import sleep
from datetime import datetime
from db.db import schedule_collection, drone_collection
from schemas.schemas import list_schedule_serial
from dotenv import load_dotenv
import os
import asyncio
from bson import ObjectId

load_dotenv()
thread_interval = int(os.getenv("THREAD_INTERVAL"))


async def mission_firing_thread():
    while True:
        try:
            current_datetime = datetime.utcnow()
            print(f"Current datetime: {current_datetime}")

            # Compare only the date and time components without microseconds
            missions_to_start = list_schedule_serial(schedule_collection.find({"start_time": {"$lte": current_datetime}, "status": "scheduled"}))
            print(missions_to_start)
            start_tasks = []
            for mission in missions_to_start:
                # Update drone status to "on a mission"
                start_tasks.append(drone_collection.update_one({"_id": ObjectId(mission["drone_id"])}, {"$set": {"status": "on-mission"}}))
                # Update mission status to "in progress"
                start_tasks.append(schedule_collection.update_one({"mission_id": mission["mission_id"]}, {"$set": {"status": "in-progress"}}))

            # Check for missions that have ended and update statuses
            missions_to_complete = list_schedule_serial(schedule_collection.find({"end_time": {"$lte": current_datetime}, "status": "in-progress"}))
            complete_tasks = []
            for mission in missions_to_complete:
                # Update drone status to "available"
                complete_tasks.append(drone_collection.update_one({"_id": ObjectId(mission["drone_id"])}, {"$set": {"status": "available"}}))
                # Update mission status to "completed"
                complete_tasks.append(schedule_collection.update_one({"mission_id": mission["mission_id"]}, {"$set": {"status": "completed"}}))

            await asyncio.gather(*complete_tasks, *complete_tasks)
            await asyncio.sleep(thread_interval)
        except Exception as e:
            print(f"An error occurred: {e}")

