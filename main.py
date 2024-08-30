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
    
    def  getSOC(self):
        return self.remain_energy / self.BATTERY_CAPACITY
    
    def func1_getChargeCost(self, _energy, _time: int ):
        PRICE_PER_CHARGE: float = 1.0
        NIGHT_PRICE_RATIO: float = 2.0
        
        _energy = self.remainEnergy
        price = _energy * PRICE_PER_CHARGE
        
        if _time % 24 < 9: # NIGHT Price
            return price * NIGHT_PRICE_RATIO
        return price # DAY Price
    
    def func2_getCostPerWear(self, _degradation: float, _value: float):
        return _degradation * _value
    
    def func3_getStationCost(self):
        station_price = 1.0
        return station_price
        
    def func7_getTravelEnergyCost(self, _distance: float) -> float:
        ALPHA = 0.6
        dischargeEnergy = ALPHA * self.WEIGHT * _distance
        
        return dischargeEnergy
    
    def func8_getReturnStationEnergy(self, _remain_energy, _travel_energy_cost, _distance):
        remain_energy = self.remain_energy
        travel_energy_cost = self.func7_getTravelEnergyCost(_distance)
        return remain_energy - travel_energy_cost, travel_energy_cost
    
    def func9_getDegradation(self, _remain_energy):
        HEALTH_SOC_MIN, HEALTH_SOC_MAX  = self.HEALTH_SOC
        DEGRADATION = 0.8
        
        if HEALTH_SOC_MIN <= self.soc <= HEALTH_SOC_MAX:
            return DEGRADATION # health-charged
        
        return DEGRADATION * 2 # over-charged
    
    def func11_getHealthDegradation(self, _remain_energy, _energy_cost):
        cycle_life = 1
        DoD = _energy_cost / self.BATTERY_CAPACITY
        HEALTH_SOC_MIN, HEALTH_SOC_MAX  = self.HEALTH_SOC
        
        numerator = abs( HEALTH_SOC_MAX - self.remain_energy )
        denominator = cycle_life * (DoD / 1.0) * self.BATTERY_CAPACITY
        
        health_degradation = numerator / denominator
        return health_degradation
        
class Schedule:
    def __init__(self, _fleets: list[Vehicle] = [] ):
        self.fleets: list[Vehicle] = _fleets
        # self.HEALTH_SOC: list[float] = [20, 80]
        
    def setFleets(self, _fleet: list[Vehicle] ):
        for vehicle in _fleet:
            self.fleets.append(vehicle)
    
    
    
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