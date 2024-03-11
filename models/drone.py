from pydantic import BaseModel
from typing import List, Union

class DroneModel(BaseModel):
    name: str
    status: str
    current_mission_id: int | None = None
    possible_missions_ids: List[int]
    
    class Config:
        orm_mode = True
