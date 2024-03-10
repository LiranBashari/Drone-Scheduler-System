from pydantic import BaseModel

class TrajectoryModel(BaseModel):
    description: str
    type: str
    number_of_products: int

    class Config:
        orm_mode = True