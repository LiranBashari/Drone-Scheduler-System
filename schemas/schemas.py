from models.drone import DroneModel
from models.trajectory import TrajectoryModel
from models.mission import MissionModel
from models.schedule import ScheduleModel

def individual_drone_serial(drone) -> dict:
    return {
        "id": str(drone["_id"]),
        "name": drone["name"],
        "status": drone["status"],
        "current_mission_id": drone["current_mission_id"],
        "possible_missions_ids": drone["possible_missions_ids"]
    }


def list_drone_serial(drones) -> list:
    return [individual_drone_serial(d) for d in drones]


def convert_trajectory_to_schema(trajectory: TrajectoryModel) -> dict:
    return {
        'id': str(trajectory.id),
        'description': trajectory.description,
        'type': trajectory.type,
        'number_of_products': trajectory.number_of_products
    }

def convert_mission_to_schema(mission: MissionModel) -> dict:
    return {
        'id': str(mission.id),
        'trajectory_id': mission.trajectory_id,
        'duration': mission.duration,
        'priority': mission.priority
    }

def convert_schedule_to_schema(schedule: ScheduleModel) -> dict:
    return {
        'id': str(schedule.id),
        'drone_id': schedule.drone_id,
        'mission_id': schedule.mission_id,
        'start_time': schedule.start_time,
        'end_time': schedule.end_time,
        'status': schedule.status
    }
