from enum import Enum

class VehicleState(Enum):
    IDLE = 0
    TRAVEL = 1
    CHARGING = 2

class VehicleType():
    def __init__(self, _name:str, _value: float, _weight: float, _battery: float):
        self.name: str = _name
        self.value: float = _value
        self.weight: float = _weight
        self.battery: float = _battery
        
    def __repr__(self):
        return f"VehicleType: {self.name: <15} Weight: {self.weight: <8} Battery: {self.battery: <8}"

class Vehicle:
    HEALTH_SOC = [0.2, 0.8]
    ALPHA = 0.6
    
    def __init__(self, 
                 _id:               str = None,
                 _vehicle_type:     VehicleType = None,
                 _vehicle_value:    float = None,
                 _weight:           float = None,
                 _battery:          float = None
                 # _alpha:            float = None
                 ) -> None:
        # Constant informations
        self.ID: str = _id
        self.VEHICLE_TYPE: VehicleType = _vehicle_type
        
        # use vehicleType's default value if not given in constructor
        self.VEHICLE_VALUE: float    = _vehicle_value if _vehicle_value != None else _vehicle_type.value
        self.WEIGHT: float           = _weight  if _weight  != None else _vehicle_type.weight
        self.BATTERY_CAPACITY: float = _battery if _battery != None else _vehicle_type.battery
        
        # charger information
        self.charger_id: str = None
        
        # member variables
        # self.cycle_life = 1
        self.soc: float = 100.0
        self.remain_energy: float = self.BATTERY_CAPACITY
        self.state: VehicleState = VehicleState.IDLE
        self.start_time: int = 0
        self.idle_time: int = 0
        pass
    
    def __repr__(self):
        return f"Vehicle: {self.ID: <8} State: {self.state.name: <10} (soc: {self.soc:<4.2f}) IdleTime: {self.idle_time: <4} Battery: {self.remain_energy: <8} / {self.BATTERY_CAPACITY: <8} "
    
    def reset(self):
        self.soc = 100
        self.remain_energy = self.BATTERY_CAPACITY
        self.state = VehicleState.IDLE
        self.start_time = 0
        self.idle_time = 0
    
    def getSOC(self):
        return self.remain_energy / self.BATTERY_CAPACITY * 100
    
    def travel(self, _distance: float, _travel_start_time: int):
        if self.state == VehicleState.TRAVEL:
            raise ValueError( f"Time ({_travel_start_time}) {self.ID}: Vehicle is already in travel state" )
        
        self.state = VehicleState.TRAVEL
        self.idle_time = _travel_start_time
        
        # if travel used energy < remain_energy, return a error
        if self.__func8_getReturnStationEnergy(_distance) < 0:
            raise ValueError( f"Time ({_travel_start_time}) {self.ID}: remain energy not enough: {self.remain_energy} < {self.__func7_getTravelEnergy(_distance)}" )
        
        self.remain_energy = self.__func8_getReturnStationEnergy(_distance)
        self.soc = self.getSOC()
    
    def returnStation(self):
        self.state = VehicleState.IDLE
        # return self.remain_energy
    
    def plugVehicle(self, _start_time: int, _charger_id: str):
        self.state = VehicleState.CHARGING
        self.charger_id = _charger_id
        self.start_time = _start_time
        
    def chargeBattery(self, _charge_energy: float):
        self.remain_energy += _charge_energy
        if self.remain_energy > self.BATTERY_CAPACITY:
            self.remain_energy = self.BATTERY_CAPACITY
        self.soc = self.getSOC()
    
    def unplugVehicle(self, _finish_time: int):
        self.state = VehicleState.IDLE
        self.charger_id = None
        self.idle_time = _finish_time
    
    def getTravelEnergy(self, _distance: float) -> float:
        return self.__func7_getTravelEnergy(_distance)
    
    
    # EC_v
    def __func7_getTravelEnergy(self, _distance: float) -> float:
        '''
        EC_v = alpha * W_v * S_v
        '''
        return self.ALPHA * self.WEIGHT * _distance
    
    # b_vt
    def __func8_getReturnStationEnergy(self, _distance: float) -> tuple[float, float]:
        '''
        b_vt = b_vt{previous} - EC_v
        '''
        # print( self.__func7_getTravelEnergy(_distance) )
        return self.remain_energy - self.__func7_getTravelEnergy(_distance)        

    
    # Degradation Cost Formula Functions
    """
    
    # w_vt
    def __func2_getWearCost(self, _degradation: float, _value: float) -> float:
        '''
        w_vt = D(e_vt) * value
        W_t = sum(w_vt) for v in vehicles 
        '''
        return _degradation * _value
    
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
    """
    