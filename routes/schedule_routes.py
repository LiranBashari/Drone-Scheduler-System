from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from db.db import schedule_collection, drone_collection, mission_collection, trajectory_collection
from models.schedule import ScheduleModel
from schemas.schemas import list_schedule_serial, individual_schedule_serial, individual_drone_serial, list_mission_serial, individual_mission_serial, individual_trajectory_serial
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
    schedule = individual_schedule_serial(schedule_collection.find_one({"_id": ObjectId(id)}))
    if schedule:
        return schedule
    else:
        raise HTTPException(status_code=404, detail="Schedule not found")
    


@route.get('/drone/{id}')
async def get_schedules_by_drone_id(id: str):
    try:
        schedules = list_schedule_serial(schedule_collection.find({"drone_id": id}))
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.get('/mission/{id}')
async def get_schedules_by_mission_id(id: str):
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
    # first check edge cases before create new schedule
    await check_drone_mission_compatibility(schedule)
    await check_mission_overlap_prevention(schedule)
    await check_unique_mission_execution(schedule)
    
    try:
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
    



#  -----------------------Validations-------------------------------
    
async def check_drone_mission_compatibility(schedule):
    drone = individual_drone_serial(drone_collection.find_one({"_id": ObjectId(schedule.drone_id)}))
    if drone:
        if schedule.mission_id not in drone["possible_missions_ids"]:
            
            raise HTTPException(status_code=400, detail="Drone is not compatible with the mission")
    else:
        raise HTTPException(status_code=400, detail="Drone is not found")


async def check_mission_overlap_prevention(schedule):
    ongoing_missions = list_mission_serial(schedule_collection.find({
        "drone_id": schedule.drone_id,
        "start_time": {"$lt": schedule.end_time},
        "end_time": {"$gte": schedule.start_time}
    }))

    if len(ongoing_missions) > 0:
        raise HTTPException(status_code=409, detail="Drone cannot be assigned to two missions simultaneously")

async def check_unique_mission_execution(schedule):
    missions_description = set()
    schedules_within_the_range = list_mission_serial(mission_collection.find({
        "start_time": {"$lt": schedule.end_time},
        "end_time": {"$gt": schedule.start_time}
    }))
    print(schedules_within_the_range)
    if schedules_within_the_range:
        for s in schedules_within_the_range:
            mission = mission_collection.find_one({"_id": ObjectId(s.mission_id)})
            if mission:
                trajectory = trajectory_collection.find_one({"_id": ObjectId(mission.trajectory_id)})
                if trajectory:
                    description = trajectory.description
                    if description in missions_description:
                        raise HTTPException(status_code=409, detail="Two missions with the same description cannot be executed at the same time")
                    else:
                        missions_description.add(description)
    return True


        
