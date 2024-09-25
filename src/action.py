from enum import Enum

class Schedule:
    def __init__(self,
                 _start_time: int,
                 _end_time: int,
                 _vehicle_id: str,
                 _distance: float
                 ) -> None:
        self.START_TIME = _start_time
        self.END_TIME = _end_time
        self.VEHICLE_ID = _vehicle_id
        self.DISTANCE = _distance
        self.finished: bool = False
        pass

# Enum to differentiate between start and end Actions
class ActionType(Enum):
    START = "start"
    END = "end"

# Action class to represent a schedule's start or end Action
class Action:
    def __init__(self, time: int, action_type: ActionType, schedule: Schedule) -> None:
        self.time = time
        self.action_type = action_type
        self.schedule = schedule
    
    def __repr__(self):
        if self.action_type == ActionType.START:
            return f"Time: {self.time: <5} Vehicle: {self.schedule.VEHICLE_ID: <8} Action {self.action_type.name: <7} distance: {self.schedule.DISTANCE: <4} finished: {str(self.schedule.finished): <5}"
        elif self.action_type == ActionType.END:
            return f"Time: {self.time: <5} Vehicle: {self.schedule.VEHICLE_ID: <8} Action {self.action_type.name: <7}"
        