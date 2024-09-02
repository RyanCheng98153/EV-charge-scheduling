from src.vehicle import Vehicle, VehicleState
from enum import Enum

class StationState(Enum):
    IDLE = 0
    CHARGING = 1

class Station:
    PRICE_PER_CHARGE: float = 1.0
    NIGHT_PRICE_RATIO: float = 2.0
    
    def __init__(self, 
                 _id:                   str, 
                 _station_value:        float = 10000.0, 
                 _charge_rate_per_time: float = 1.0
                 ) -> None:
        # Constant informations
        self.ID: str = _id
        self.STATION_VALUE: float = _station_value
        self.CHARGE_RATE_PER_TIME: float = _charge_rate_per_time
        
        # member variables
        self.vehicle: Vehicle = None
        self.state = StationState.IDLE
        
        self.idle_time: int = 0
        
        self.charge_time: int = 0
        self.charge_energy: float = 0.0
        self.charge_cost: float = 0.0
        pass
    
    def printStationInfo(self):
        print(f"station: {self.ID: <8} state: {self.state.name: <10} vehicle: {'None' if self.vehicle == None else self.vehicle.ID: <8} charge rate: {self.CHARGE_RATE_PER_TIME}")
    
    def chargeVehicle(self, _vehicle: Vehicle, _start_time: int, _charge_energy: float) -> None:
        self.vehicle = _vehicle
        if _charge_energy + _vehicle.remain_energy > _vehicle.BATTERY_CAPACITY:
            self.charge_energy = self.vehicle.BATTERY_CAPACITY - self.vehicle.remain_energy
        else:
            self.charge_energy = _charge_energy
            
        self.charge_cost, self.charge_time = self.__func1_getChargeCost(_start_time, self.charge_energy)
        
        self.state = StationState.CHARGING
        self.idle_time = _start_time + self.charge_time
        self.vehicle.state = VehicleState.CHARGING
        self.vehicle.idle_time = self.idle_time
        
        self.vehicle.chargeBattery(self.charge_energy)
        
        
    def leaveStation(self) -> tuple[int, float, float]:
        self.vehicle.state = VehicleState.IDLE
        self.vehicle = None
        
        charge_time = self.charge_time
        charge_cost = self.charge_cost
        charge_energy = self.charge_energy
        
        self.charge_time = 0
        self.charge_energy = 0.0
        self.charge_cost = 0.0
        
        return charge_time, charge_energy, charge_cost
    
    # P_cs
    def __func3_getStationValue(self) -> float:
        return self.STATION_VALUE
    
    # E_t
    def __func1_getChargeCost(self, _start_time: int, _charge_energy: float) -> tuple[float, int]:
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
                night_time += 36
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