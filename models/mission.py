from pydantic import BaseModel

class MissionModel(BaseModel):
    trajectory_id: str
    duration: int
    priority: int

    class Config:
        orm_mode = True