from pydantic import BaseModel
from datetime import datetime

class ScheduleModel(BaseModel):
    drone_id: int
    mission_id: int
    start_time: datetime
    end_time: datetime
    status: str
    
    class Config:
        orm_mode = True