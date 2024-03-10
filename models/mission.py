from pydantic import BaseModel

class MissionModel(BaseModel):
    trajectory_id: int
    duration: int
    priority: int

    class Config:
        orm_mode = True