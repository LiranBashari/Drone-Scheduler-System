from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from db.db import drone_collection
from models.drone import DroneModel
from schemas.schemas import list_drone_serial, individual_drone_serial
from bson import ObjectId

route = APIRouter()

@route.get('/')
async def get_all_drones():
    try:
        return list_drone_serial(drone_collection.find())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.get('/{id}')
async def get_drone_by_id(id: str):
    drone = individual_drone_serial(drone_collection.find_one({"_id": ObjectId(id)}))
    if drone:
        return drone
    else:
        raise HTTPException(status_code=404, detail="Drone not found")
    


@route.get('/status/{status}')
async def get_drones_by_status(status: str):
    try:
        return list_drone_serial(drone_collection.find({"status": status}))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.post('/add')
async def add_new_drone(drone: DroneModel):
    try:
        drone_collection.insert_one(dict(drone))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Validation Error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.put("/update/{id}")
async def update_drone_by_id(id: str, drone: DroneModel):
    result = drone_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(drone)})
    if not result:
        raise HTTPException(status_code=404, detail="Drone not found")



@route.delete("/delete/{id}")
async def delete_drone_by_id(id: str):
    result = drone_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Drone not found")
    