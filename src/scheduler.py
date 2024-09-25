from src.vehicle import Vehicle
from src.station import Station
from src.action import Action, Schedule, ActionType

class Scheduler:
    def __init__(self):
        self.vehicles: dict[Vehicle] = dict()
        self.stations: dict[Station] = dict()
        
        Station.PRICE_PER_CHARGE = 1.0
        Station.NIGHT_PRICE_RATIO = 2.0
        
        self.TIMESLOTS = 672
        self.schedule_table: list[Schedule] = []
        self.action_table: list[Action] = []
    
    def operate(self):
        pass
    
    def setVehicles(self, _vehicles: list[Vehicle] ):
        print(type(self.vehicles))
        for vehicle in _vehicles:
            self.vehicles[vehicle.ID] = vehicle
        # self.vehicles = _vehicles
        
    def setStations(self, _stations: list[Station] ):
        for station in _stations:
            self.stations[station.ID] = station
        # self.stations = _stations
        
    def setSchedules(self, _schedule_table: list[Schedule]):
        self.schedule_table = _schedule_table
        self.schedule_table = sorted(self.schedule_table, key=lambda schedule: schedule.END_TIME, reverse=False)
        self.schedule_table = sorted(self.schedule_table, key=lambda schedule: schedule.START_TIME, reverse=False)
        
    def createActionTable(self):
        action_table = []
        for schedule in self.schedule_table:
            start_action = Action(schedule.START_TIME, ActionType.START, schedule)
            action_table.append(start_action)
            self.vehicles[schedule.VEHICLE_ID].action_table.append(start_action)
            end_action = Action(schedule.END_TIME, ActionType.END, schedule)
            action_table.append(end_action)
            self.vehicles[schedule.VEHICLE_ID].action_table.append(end_action)
            
        # Sort Actions by time
        self.action_table = sorted(action_table, key=lambda Action: Action.time)
        for vehicle in self.vehicles.values():
            vehicle.action_table = sorted(vehicle.action_table, key=lambda Action: Action.time)
    
    def getVehicleById(self, _id):
        for vehicle in self.vehicles:
            if vehicle.ID == _id:
                return vehicle
        
    def printScheduleTable(self):
        print("[Schedule Table]")
        for schedule in self.schedule_table:
            print(f"start: {schedule.START_TIME: <5} end: {schedule.END_TIME: <5} vehicle: {schedule.VEHICLE_ID: <10} distance: {schedule.DISTANCE: <8} finished: {str(schedule.finished): <5}")
        print()
        
    def printActionTable(self):
        print("[Action Table]")
        for action in self.action_table:
            print(action)
        print()
        
    def printVehicles(self):
        print("[Vehicle]")
        for vehicle in self.vehicles.values():
            vehicle.printVehicleInfo()
        print()
    
    def printStations(self):
        print("[Station]")
        for station in self.stations.values():
            station.printStationInfo()
        print()
        