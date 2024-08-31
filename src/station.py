from src.vehicle import Vehicle

class Station:
    def __init__(self, 
                 _id:               int, 
                 _station_value:    float = 10000.0, 
                 _charge_rate_hour: float = 1.0
                 ) -> None:
        self.vehicle: Vehicle = None
        self.charge_energy: float = 0.0
        self.charge_fee: float = 0.0
        
        self.start_time: int = 0.0
        self.finish_time: int = 0.0
        
        # Constant informations
        self.ID: int = _id
        self.STATION_VALUE: float = _station_value
        self.CHARGE_RATE_HOUR: float = _charge_rate_hour
        
        pass
    
    # P_cs
    def func3_getStationValue(self) -> float:
        return self.STATION_VALUE
    
    # E_t
    def func1_getChargeCost(self, _charge_energy: float, _time: int ):
        price = _charge_energy * self.PRICE_PER_CHARGE
        
        if _time % 24 < 9: # NIGHT Price
            return price * self.NIGHT_PRICE_RATIO
        return price # DAY Price

    def chargeVehicle(self, _vehicle:Vehicle, _energy: float, _start_time: int) -> bool:
        if self.vehicle != None:
            return False
        
        self.vehicle = _vehicle
        self.charge_energy: float = _energy
        
        used_time = _energy / self.CHARGE_RATE_HOUR 
        self.start_time = _start_time
        self.finish_time = _start_time + used_time
        return True
    
    def leaveStation(self):
        self.vehicle = None
        
        energy = self.charge_energy
        self.charge_energy = 0.0
        
        # require a function to count the day and night energy
        
        return energy