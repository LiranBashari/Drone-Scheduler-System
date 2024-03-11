from fastapi import FastAPI
from db.db import client
from routes import drone_routes, trajectory_routes, mission_routes, schedule_routes

app = FastAPI()

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


app.include_router(drone_routes.route, prefix="/drones")
app.include_router(trajectory_routes.route, prefix="/trajectory")
app.include_router(mission_routes.route, prefix="/mission")
app.include_router(schedule_routes.route, prefix="/schedule")
