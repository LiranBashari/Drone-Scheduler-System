from pydantic import BaseModel
from typing import List, Union

class DroneModel(BaseModel):
    name: str
    status: str
    current_mission_id: str | None = None
    possible_missions_ids: List[str]
    
    class Config:
        orm_mode = True
