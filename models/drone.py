from pydantic import BaseModel
from typing import List

class DroneModel(BaseModel):
    name: str
    status: str
    current_mission_id: int
    possible_missions_ids: List[int]
    
    class Config:
        orm_mode = True