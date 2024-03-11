from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from db.db import schedule_collection
from models.schedule import ScheduleModel
from schemas.schemas import list_schedule_serial
from bson import ObjectId
from datetime import datetime

route = APIRouter()

@route.get('/')
async def get_all_schedules():
    try:
        return list_schedule_serial(schedule_collection.find())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.get('/{id}')
async def get_schedule_by_id(id: str):
    schedule = schedule_collection.find_one({"_id": ObjectId(id)})
    if schedule:
        return schedule
    else:
        raise HTTPException(status_code=404, detail="Schedule not found")
    


@route.get('/drones/{id}')
async def get_schedules_by_drone_id(id: int):
    try:
        schedules = list_schedule_serial(schedule_collection.find({"drone_id": id}))
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.get('/missions/{id}')
async def get_schedules_by_mission_id(id: int):
    try:
        schedules = list_schedule_serial(schedule_collection.find({"mission_id": id}))
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@route.get('/status/{status}')
async def get_schedules_by_status(status: str):
    try:
        schedules = list_schedule_serial(schedule_collection.find({"status": status}))
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.post('/range')
async def get_schedules_within_range(start_date: str, end_date: str):
    try:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f")
        schedules = list_schedule_serial(schedule_collection.find({"start_time": {"$gte": start_datetime}, "end_time": {"$lte": end_datetime}}))
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.post('/add')
async def add_new_schedule(schedule: ScheduleModel):
    try:
        # Check if the drone is already booked for another mission during the same time frame
        overlapping_missions = schedule_collection.find({
            "drone_id": schedule.drone_id,
            "start_time": {"$lte": schedule.end_time},
            "end_time": {"$gte": schedule.start_time}
        })

        if overlapping_missions.count() > 0:
            raise HTTPException(status_code=409, detail="Drone already booked for another mission")
        
        # "mission firing" mechanism - Update the drone's status in the database
        schedule_collection.update_one(
            {"drone_id": schedule.drone_id, "start_time": schedule.start_time},
            {"$set": {"status": "on-mission"}}
        )

        #  A notification when scheduled drone is going on its mission
        print(f"Alert: Drone {schedule.drone_id} is going on a mission at {schedule.start_time}")
        
        # Insert the new mission into the database
        schedule_collection.insert_one(dict(schedule))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Validation Error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.put("/update/{id}")
async def update_schedule_by_id(id: str, schedule: ScheduleModel):
    result = schedule_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(schedule)})
    if not result:
        raise HTTPException(status_code=404, detail="Schedule not found")



@route.delete("/delete/{id}")
async def delete_schedule_by_id(id: str):
    result = schedule_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Schedule not found")
    