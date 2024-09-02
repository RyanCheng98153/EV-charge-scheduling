from src.vehicle import Vehicle
from src.station import Station

class Schedule:
    def __init__(self,
                 _start_time: int,
                 _end_time: int,
                 _vehicle_id: int,
                 _distance: float
                 ) -> None:
        self.START_TIME = _start_time
        self.END_TIME = _end_time
        self.VEHICLE_ID = _vehicle_id
        self.DISTANCE = _distance
        pass

class Scheduler:
    def __init__(self ):
        self.fleets: list[Vehicle] = []
        self.stations: list[Station] = []
        
        Station.PRICE_PER_CHARGE = 1.0
        Station.NIGHT_PRICE_RATIO = 2.0
        
        self.TIMESLOTS = 672
        self.schedule_table: list[Schedule] = [
            Schedule(0, 100, 1,12),
            Schedule(200, 350, 1, 20),
        ]
        self.action_table: list[dict] = []
        
    def setFleets(self, _fleet: list[Vehicle] ):
        for vehicle in _fleet:
            self.fleets.append(vehicle)
    
    def setStations(self, _stations: list[Station] ):
        for station in _stations:
            self.stations.append(station)
    
    def CreateActionTable(self):
        action_table = []
        for schedule in self.schedule_table:
            action_table.append({"time": schedule.START_TIME, "vehicle_id": schedule.VEHICLE_ID, "distance": -1})
            action_table.append({"time": schedule.END_TIME, "vehicle_id": schedule.VEHICLE_ID, "distance": schedule.DISTANCE})
        self.action_table = sorted(action_table, key=lambda action:action["time"], reverse=False)
        
    def PrintScheduleTable(self):
        for schedule in self.schedule_table:
            print(f"start: {schedule.START_TIME}, end: {schedule.END_TIME}, vehicle: {schedule.VEHICLE_ID}, distance: {schedule.DISTANCE}")
            
    def PrintActionTable(self):
        for action in self.action_table:
            print(f"time: {action['time']}, vehicle_id: {action['vehicle_id']}, distance: {action['distance']}")