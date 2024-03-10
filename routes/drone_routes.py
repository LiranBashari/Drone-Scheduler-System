from fastapi import APIRouter
from db.db import client
from bson import ObjectId
from db.db import drone_collection
from schemas.schemas import list_drone_serial

route = APIRouter()

@route.get('/')
async def get_all_drones():
    drones = list_drone_serial(drone_collection.find())
    return drones
