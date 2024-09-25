from enum import Enum
from src.action import Action

class VehicleState(Enum):
    IDLE = 0
    TRAVEL = 1
    CHARGING = 2

class Vehicle:
    def __init__(self, 
                 _id:               str,
                 _vehicle_value:    float,
                 _weight:           float,
                 _battery:          float,
                 ) -> None:
        # Constant informations
        self.ID: str = _id
        self.VEHICLE_VALUE:float = _vehicle_value
        self.WEIGHT: float = _weight
        self.BATTERY_CAPACITY: float = _battery
        self.HEALTH_SOC = [0.2, 0.8]
        self.ALPHA = 0.6
        self.action_table: list[Action] = []
        
        # member variables
        self.cycle_life = 1
        self.soc: float = 100
        self.remain_energy: float = _battery
        self.state: VehicleState = VehicleState.IDLE
        self.idle_time: int = 0
        pass
    
    def printVehicleInfo(self):
        print(f"vehicle: {self.ID: <8} state: {self.state.name: <10} idle time: {self.idle_time:<8} battery: {self.remain_energy: <8} / {self.BATTERY_CAPACITY: <8} (soc: {self.soc})")
    
    def getSOC(self):
        return self.remain_energy / self.BATTERY_CAPACITY
    
    def getTravelEnergy(self, _distance: float):
        return self.__func7_getTravelEnergyCost(_distance)
    
    def travel(self, _distance: float, _travel_time: int):
        self.state = VehicleState.TRAVEL
        self.idle_time = _travel_time
        self.remain_energy = self.__func8_getReturnStationEnergy(_distance)
        self.soc = self.getSOC()
    
    def chargeBattery(self, _charge_energy: float, _idle_time: int):
        self.state = VehicleState.CHARGING
        self.remain_energy += _charge_energy
        if self.remain_energy > self.BATTERY_CAPACITY:
            self.remain_energy = self.BATTERY_CAPACITY
        self.soc = self.getSOC()
        self.idle_time = _idle_time
    
    def returnStation(self):
        self.state = VehicleState.IDLE
        return self.remain_energy
        
    # w_vt
    def __func2_getWearCost(self, _degradation: float, _value: float) -> float:
        '''
        w_vt = D(e_vt) * value
        W_t = sum(w_vt) for v in vehicles 
        '''
        return _degradation * _value
    
    # EC_v
    def __func7_getTravelEnergyCost(self, _distance: float) -> float:
        '''
        EC_v = alpha * W_v * S_v
        '''
        dischargeEnergy = self.ALPHA * self.WEIGHT * _distance
        return dischargeEnergy
    
    # b_vt
    def __func8_getReturnStationEnergy(self, _distance: float) -> tuple[float, float]:
        '''
        b_vt = b_vt{previous} - EC_v
        '''
        travel_energy_cost = self.__func7_getTravelEnergyCost(_distance)
        return self.remain_energy - travel_energy_cost
    
    # D(e_vt)
    def __func9_getDegradation(self, _charge_energy: float) -> float:
        '''
        D(e_vt) = soc in range [HealthSOC] -> DCH, otherwise -> 2 * DCH
        '''
        HEALTH_SOC_MIN, HEALTH_SOC_MAX  = self.HEALTH_SOC
        DEGRADATION = self.__func11_getHealthDegradation(_charge_energy)
        
        if HEALTH_SOC_MIN <= self.soc <= HEALTH_SOC_MAX:
            return DEGRADATION # health-charged
        return DEGRADATION * 2 # over-charged
    
    # DCH
    def __func11_getHealthDegradation(self, _charge_energy: float) -> float:
        '''
        abs(HealthSOC_max - b_vt) / (CL * (DoD / 100%) * B)
        '''
        DoD = _charge_energy / self.BATTERY_CAPACITY
        HEALTH_SOC_MIN, HEALTH_SOC_MAX  = self.HEALTH_SOC
        
        numerator = abs( HEALTH_SOC_MAX - self.remain_energy )
        denominator = self.cycle_life * (DoD / 1.0) * self.BATTERY_CAPACITY
        
        health_degradation = numerator / denominator
        return health_degradation
    
    