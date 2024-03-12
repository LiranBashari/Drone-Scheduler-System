from pydantic import BaseModel
from datetime import datetime

class ScheduleModel(BaseModel):
    drone_id: str
    mission_id: str
    start_time: datetime
    end_time: datetime
    status: str
    
    class Config:
        orm_mode = True