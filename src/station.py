from src.vehicle import Vehicle
from enum import Enum

class StationState:
    IDLE = 0
    CHARGING = 1

class Station:
    PRICE_PER_CHARGE: float = None
    NIGHT_PRICE_RATIO: float = None
    
    def __init__(self, 
                 _id:                   int, 
                 _station_value:        float = 10000.0, 
                 _charge_rate_per_time: float = 1.0
                 ) -> None:
        self.vehicle: Vehicle = None
        self.charge_energy: float = 0.0
        self.charge_fee: float = 0.0
        
        self.start_time: int = 0.0
        self.finish_time: int = 0.0
        
        # Constant informations
        self.ID: int = _id
        self.STATION_VALUE: float = _station_value
        self.CHARGE_RATE_PER_TIME: float = _charge_rate_per_time
        
        pass
    
    # P_cs
    def func3_getStationValue(self) -> float:
        return self.STATION_VALUE
    
    # E_t
    def func1_getChargeCost(self, _charge_energy: float, _start_time: int ):
        charge_time = _charge_energy / self.CHARGE_RATE_PER_TIME
        
        # timeslot: 24 hours = 96 timeslot, 9 hours = 36 timeslot
        day_time = charge_time // 96 * 60
        night_time = charge_time // 96 * 36
        # rest of the time: 96 time 
        rest_time = charge_time % 96
        
        # start day time 
        if _start_time >= 36: 
            # end day time
            if _start_time + rest_time < 96: 
                day_time += rest_time
            # end next night time
            elif 96 <= _start_time + rest_time < 96 + 36: 
                day_time += 132 - _start_time # 96 + 36 - _start_time
                night_time += rest_time - 132
            # end next day time
            elif _start_time + rest_time >= 96 + 36: 
                # day_time += ( 96 - _start_time ) + ( _start_time + rest_time - 132 )
                day_time += rest_time - 36
                night_energy += 36
        # start night time 
        elif _start_time < 36: 
            # end night time
            if _start_time + rest_time < 36:
                night_time += rest_time
            # end day time
            elif 36 <= _start_time + rest_time < 96: 
                day_time += rest_time - 36
                night_time += 36 - _start_time
            # end next night time
            elif _start_time + rest_time >= 96: 
                day_time += 60
                # day_time += 36 - _start_time + _start_time + rest_time - 96
                night_time += rest_time - 60
            
        # 1 day has 15 hours (60 timeslot) and 9 hours (36 timeslot)
        day_energy_cost = day_time * self.CHARGE_RATE_PER_TIME * self.PRICE_PER_CHARGE
        night_energy_cost = night_time * self.CHARGE_RATE_PER_TIME  * self.PRICE_PER_CHARGE * self.NIGHT_PRICE_RATIO
        
        return day_energy_cost + night_energy_cost, charge_time
    
    def leaveStation(self):
        self.vehicle = None
        
        energy = self.charge_energy
        self.charge_energy = 0.0
        
        # require a function to count the day and night energy
        
        return energy