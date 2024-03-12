from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from db.db import mission_collection, trajectory_collection
from models.mission import MissionModel
from schemas.schemas import list_mission_serial, individual_mission_serial, individual_trajectory_serial
from bson import ObjectId

route = APIRouter()

@route.get('/')
async def get_all_missions():
    try: 
        return list_mission_serial(mission_collection.find())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.get('/{id}')
async def get_mission_by_id(id: str):
    mission = mission_collection.find_one({"_id": ObjectId(id)})
    if mission:
        return individual_mission_serial(mission)
    else:
        raise HTTPException(status_code=404, detail="Mission not found")    



@route.get('/trajectory/{id}')
async def get_mission_trajectory_by_id(id: str):
    mission = mission_collection.find_one({"trajectory_id": id})
    if mission:
        mission_trajectory = individual_trajectory_serial(trajectory_collection.find_one({"_id": ObjectId(mission["trajectory_id"])}))
        if mission_trajectory:
            return mission_trajectory
        else:
            raise HTTPException(status_code=404, detail="Trajectory not found")
    else:
        raise HTTPException(status_code=404, detail="Mission not found")



@route.get('/priority/highest')
async def get_mission_by_highest_priority():
    missions = list_mission_serial(mission_collection.find().sort("priority", -1).limit(1))
    return missions[0] if missions else None



@route.post('/add')
async def add_new_mission(mission: MissionModel):
    try:
        mission_collection.insert_one(dict(mission))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Validation Error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.put("/update/{id}")
async def update_mission_by_id(id: str, mission: MissionModel):
    result = mission_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(mission)})
    if not result:
        raise HTTPException(status_code=404, detail="Mission not found")



@route.put("/update/priority/{id}")
async def update_mission_priority_by_id(id: str, mission: MissionModel):
    result = mission_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"priority": mission.priority}})
    if not result:
        raise HTTPException(status_code=404, detail="Mission not found")



@route.delete("/delete/{id}")
async def delete_mission_by_id(id: str):
    result = mission_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Mission not found")