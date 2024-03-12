from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from db.db import trajectory_collection
from models.trajectory import TrajectoryModel
from schemas.schemas import list_trajectory_serial, individual_trajectory_serial
from bson import ObjectId

route = APIRouter()

@route.get('/')
async def get_all_trajectories():
    try: 
        return list_trajectory_serial(trajectory_collection.find())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.get('/{id}')
async def get_trajectory_by_id(id: str):
    trajectory = individual_trajectory_serial(trajectory_collection.find_one({"_id": ObjectId(id)}))
    if trajectory:
        return trajectory
    else:
        raise HTTPException(status_code=404, detail="Trajectory not found")



@route.get('/type/{type}')
async def get_trajectory_by_type(type: str):
    try: 
        trajectories = list_trajectory_serial(trajectory_collection.find({"type": type}))
        return trajectories
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.post('/add')
async def add_new_trajectory(trajectory: TrajectoryModel):
    try:
        trajectory_collection.insert_one(dict(trajectory))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Validation Error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@route.put("/update/{id}")
async def update_trajectory_by_id(id: str, trajectory: TrajectoryModel):
    result = trajectory_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(trajectory)})
    if not result:
        raise HTTPException(status_code=404, detail="Trajectory not found")



@route.put("/update/products/{id}")
async def update_trajectory_products_by_id(id: str, trajectory: TrajectoryModel):
    result = trajectory_collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": {"number_of_products": trajectory.number_of_products}})
    if not result:
        raise HTTPException(status_code=404, detail="Trajectory not found")



@route.delete("/delete/{id}")
async def delete_trajectory_by_id(id: str):
    result = trajectory_collection.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Trajectory not found")