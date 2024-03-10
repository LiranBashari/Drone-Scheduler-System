from fastapi import APIRouter
from db.db import drone_collection
from models.drone import DroneModel
from schemas.schemas import list_drone_serial
from bson import ObjectId

route = APIRouter()

@route.get('/')
async def get_all_drones():
    drones = list_drone_serial(drone_collection.find())
    return drones


@route.post('/add')
async def add_new_drone(drone: DroneModel):
    drone_collection.insert_one(dict(drone))


@route.put("/update/{id}")
async def update_drone_by_id(id: str, drone: DroneModel):
    drone_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(drone)})


@route.delete("/delete/{id}")
async def delete_by_id(id: str):
    drone_collection.find_one_and_delete({"_id": ObjectId(id)})