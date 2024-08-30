from src.vehicle import Vehicle
from src.station import Station

class Schedule:
    def __init__(self ):
        self.fleets: list[Vehicle] = []
        self.stations: list[Station] = []
        
        self.PRICE_PER_CHARGE: float = 1.0
        self.NIGHT_PRICE_RATIO: float = 2.0
        
    def setFleets(self, _fleet: list[Vehicle] ):
        for vehicle in _fleet:
            self.fleets.append(vehicle)
    
    def setStations(self, _stations: list[Station] ):
        for station in _stations:
            self.stations.append(station)
    
    # E_t
    def func1_getChargeCost(self, _charge_energy: float, _time: int ):
        price = _charge_energy * self.PRICE_PER_CHARGE
        
        if _time % 24 < 9: # NIGHT Price
            return price * self.NIGHT_PRICE_RATIO
        return price # DAY Price