from models.drone import DroneModel
from models.trajectory import TrajectoryModel
from models.mission import MissionModel
from models.schedule import ScheduleModel

# -------------------------------Drone-------------------------------
def individual_drone_serial(drone) -> dict:
    return {
        "id": str(drone["_id"]),
        "name": drone["name"],
        "status": drone["status"],
        "current_mission_id": drone["current_mission_id"],
        "possible_missions_ids": drone["possible_missions_ids"]
    }


def list_drone_serial(drones: list[DroneModel]) -> list:
    return [individual_drone_serial(d) for d in drones]



# -------------------------------Trajectory-------------------------------
def individual_trajectory_serial(trajectory: TrajectoryModel) -> dict:
    return {
        "id": str(trajectory["_id"]),
        "description": trajectory["description"],
        "type": trajectory["type"],
        "number_of_products": trajectory["number_of_products"]
    }


def list_trajectory_serial(trajectories: list[TrajectoryModel]) -> list:
    return [individual_trajectory_serial(t) for t in trajectories]


# -------------------------------Mission-------------------------------
def individual_mission_serial(mission: MissionModel) -> dict:
    return {
        "id": str(mission["_id"]),
        "trajectory_id": mission["trajectory_id"],
        "duration": mission["duration"],
        "priority": mission["priority"]
    }


def list_mission_serial(missions: list[MissionModel]) -> list:
    return [individual_mission_serial(m) for m in missions]


# -------------------------------Schedule-------------------------------
def individual_schedule_serial(schedule: ScheduleModel) -> dict:
    return {
        "id": str(schedule["_id"]),
        "drone_id": schedule["drone_id"],
        "mission_id": schedule["mission_id"],
        "start_time": schedule["start_time"],
        "end_time": schedule["end_time"],
        "status": schedule["status"]
    }


def list_schedule_serial(schedules: list[ScheduleModel]) -> list:
    return [individual_schedule_serial(s) for s in schedules]