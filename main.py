from fastapi import FastAPI
from db.db import client
from routes import drone_routes

app = FastAPI()

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Include routes from different files
app.include_router(drone_routes.route, prefix="/drones")
# app.include_router(trajectory_routes.router)
# app.include_router(mission_routes.router)
# app.include_router(schedule_routes.router)
