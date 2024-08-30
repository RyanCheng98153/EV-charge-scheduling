from src.vehicle import Vehicle

class Station:
    def __init__(self) -> None:
        self.station_price: float = 10000.0
        self.charge_rate: float = 1.0
        
        self.vehicle: Vehicle = None
        self.start_time: float = 0.0
        self.finish_time: float = 0.0
        self.charge_energy: float = 0.0
        pass
    
    # P_cs
    def func3_getStationCost(self) -> float:
        return self.station_price

    def chargeVehicle(self, _vehicle:Vehicle, _energy: float, _start_time: float) -> bool:
        if self.vehicle != None:
            return False
        
        self.vehicle = _vehicle
        self.charge_energy: float = _energy
        
        used_time = _energy / self.charge_rate
        self.start_time = _start_time
        self.finish_time = _start_time + used_time
        return True
    
    def getFinishTime(self):
        if self.vehicle == None:
            return 0.0
        return self.finish_time
    
    def leaveStation(self):
        self.vehicle = None
        
        energy = self.charge_energy
        self.charge_energy = 0.0
        
        # require a function to count the day and night energy
        
        return energy