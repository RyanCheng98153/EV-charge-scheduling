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
    def __init__(self):
        self.vehicles: list[Vehicle] = []
        self.stations: list[Station] = []
        
        Station.PRICE_PER_CHARGE = 1.0
        Station.NIGHT_PRICE_RATIO = 2.0
        
        self.TIMESLOTS = 672
        self.schedule_table: list[Schedule] = []
        self.action_table: list[dict] = []
        
    def setVehicles(self, _vehicles: list[Vehicle] ):
        self.vehicles = _vehicles
        
    def setStations(self, _stations: list[Station] ):
        self.stations = _stations
        
    def setSchedules(self, _schedule_table: list[Schedule]):
        self.schedule_table = _schedule_table
        self.schedule_table = sorted(self.schedule_table, key=lambda schedule: schedule.END_TIME, reverse=False)
        self.schedule_table = sorted(self.schedule_table, key=lambda schedule: schedule.START_TIME, reverse=False)
    
    def CreateActionTable(self):
        action_table = []
        for schedule in self.schedule_table:
            action_table.append({"time": schedule.START_TIME, "vehicle_id": schedule.VEHICLE_ID, "distance": -1})
            action_table.append({"time": schedule.END_TIME, "vehicle_id": schedule.VEHICLE_ID, "distance": schedule.DISTANCE})
        self.action_table = sorted(action_table, key=lambda action:action["time"], reverse=False)
        
    def PrintScheduleTable(self):
        print("[Schedule Table]")
        for schedule in self.schedule_table:
            print(f"start: {schedule.START_TIME: <5} end: {schedule.END_TIME: <5} vehicle: {schedule.VEHICLE_ID: <10} distance: {schedule.DISTANCE: <5}")
        print()
        
    def PrintActionTable(self):
        print("[Action Table]")
        for action in self.action_table:
            print(f"time: {action['time']: <5} vehicle: {action['vehicle_id']: <10} distance: {action['distance']: <5}")
        print()
        
    def PrintVehicles(self):
        print("[Vehicle]")
        for vehicle in self.vehicles:
            vehicle.printVehicleInfo()
        print()
    
    def PrintStations(self):
        print("[Station]")
        for station in self.stations:
            station.printStationInfo()
        print()
        