from fastapi import FastAPI
from db.db import client
from routes import drone_routes, trajectory_routes, mission_routes, schedule_routes
import logging
from background_tasks import mission_firing_thread
import asyncio

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Start the mission firing thread as a background task
asyncio.create_task(mission_firing_thread())


app.include_router(drone_routes.route, prefix="/drone")
app.include_router(trajectory_routes.route, prefix="/trajectory")
app.include_router(mission_routes.route, prefix="/mission")
app.include_router(schedule_routes.route, prefix="/schedule")
