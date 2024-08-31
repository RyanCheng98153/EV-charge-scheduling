from src.vehicle import Vehicle
from src.station import Station

class Schedule:
    def __init__(self ):
        self.fleets: list[Vehicle] = []
        self.stations: list[Station] = []
        
        Station.PRICE_PER_CHARGE = 1.0
        Station.NIGHT_PRICE_RATIO = 2.0
        
    def setFleets(self, _fleet: list[Vehicle] ):
        for vehicle in _fleet:
            self.fleets.append(vehicle)
    
    def setStations(self, _stations: list[Station] ):
        for station in _stations:
            self.stations.append(station)
    