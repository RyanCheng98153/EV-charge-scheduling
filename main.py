class Vehicle:
    def __init__(self, 
                 _id: int,
                 _weight: float,
                 _battery: float,
                 ) -> None:
        
        self.ID: int = id
        self.WEIGHT: float = _weight
        self.BATTERY_CAPACITY: float = _battery
        self.HEALTH_SOC = [0.2, 0.8]
        
        self.soc: float = 100
        self.remain_energy: float = self.BATTERY_CAPACITY
    
    def getSOC(self):
        return self.remain_energy / self.BATTERY_CAPACITY
    
    # W_t
    def func2_getWearCost(self, _degradation: float, _value: float) -> float:
        return _degradation * _value
    
    # EC_v
    def func7_getTravelEnergyCost(self, _distance: float) -> float:
        ALPHA = 0.6
        dischargeEnergy = ALPHA * self.WEIGHT * _distance
        return dischargeEnergy
    
    # b_vt
    def func8_getReturnStationEnergy(self, _distance: float) -> tuple[float, float]:
        remain_energy = self.remain_energy
        travel_energy_cost = self.func7_getTravelEnergyCost(_distance)
        return remain_energy - travel_energy_cost, travel_energy_cost
    
    # D(e_vt)
    def func9_getDegradation(self, _energy_cost: float) -> float:
        HEALTH_SOC_MIN, HEALTH_SOC_MAX  = self.HEALTH_SOC
        DEGRADATION = self.func11_getHealthDegradation(_energy_cost)
        
        if HEALTH_SOC_MIN <= self.soc <= HEALTH_SOC_MAX:
            return DEGRADATION # health-charged
        return DEGRADATION * 2 # over-charged
    
    # DCH
    def func11_getHealthDegradation(self, _energy_cost: float) -> float:
        cycle_life = 1
        DoD = _energy_cost / self.BATTERY_CAPACITY
        HEALTH_SOC_MIN, HEALTH_SOC_MAX  = self.HEALTH_SOC
        
        numerator = abs( HEALTH_SOC_MAX - self.remain_energy )
        denominator = cycle_life * (DoD / 1.0) * self.BATTERY_CAPACITY
        
        health_degradation = numerator / denominator
        return health_degradation

class Station:
    def __init__(self) -> None:
        self.station_price = 10000.0
        pass
    
    # P_cs
    def func3_getStationCost(self) -> float:
        return self.station_price

class Schedule:
    def __init__(self ):
        self.fleets: list[Vehicle] = []
        self.stations: list[Station] = []
        # self.HEALTH_SOC: list[float] = [20, 80]
        
    def setFleets(self, _fleet: list[Vehicle] ):
        for vehicle in _fleet:
            self.fleets.append(vehicle)
    
    def setStations(self, _stations: list[Station] ):
        for station in _stations:
            self.stations.append(station)
    
    # E_t
    def func1_getChargeCost(self, _charge_energy: float, _time: int ):
        PRICE_PER_CHARGE: float = 1.0
        NIGHT_PRICE_RATIO: float = 2.0
        
        price = _charge_energy * PRICE_PER_CHARGE
        
        if _time % 24 < 9: # NIGHT Price
            return price * NIGHT_PRICE_RATIO
        return price # DAY Price
    

    
def main():
    print("Start")
    schedule = Schedule()
    schedule.setFleets([
        Vehicle( 0, 1000, 1000 ),
        Vehicle( 1, 2000, 1000 ),
        Vehicle( 2, 2000, 1000 ),
        Vehicle( 3, 3000, 1000 ),
        Vehicle( 4, 3000, 1000 ),
    ])
    
if __name__ == "__main__":
    main()