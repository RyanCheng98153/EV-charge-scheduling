class Vehicle:
    def __init__(self, 
                 _id: int,
                 _weight: float,
                 _battery: float,
                 ) -> None:
        
        self.ID: int = id
        self.WEIGHT: float = _weight
        self.BATTERY_CAPACITY: float = _battery
        
        self.soc: float = 100
        self.remainEnergy: float = self.BATTERY_CAPACITY
        
    def dischargeTravel(self, _distance: float) -> float:
        dischargeEnergy = self.__getDischargeEnergy( _distance)
        self.soc -= dischargeEnergy / self.BATTERY_CAPACITY
        return dischargeEnergy / self.BATTERY_CAPACITY
    
    def __getDischargeEnergy(self, _distance: float):
        ALPHA = 0.6
        return ALPHA * self.WEIGHT * _distance
    
    def getChargePrice(self, _time: int ):
        PRICE_PER_CHARGE: float = 1.0
        NIGHT_PRICE_RATIO: float = 2.0
        
        price = self.remainEnergy * PRICE_PER_CHARGE
        
        if _time % 24 < 9: # NIGHT Price
            return price * NIGHT_PRICE_RATIO
        return price # DAY Price
    
    
        
            
        
class Schedule:
    def __init__(self, _fleets: list[Vehicle] = [] ):
        self.fleets: list[Vehicle] = _fleets
        self.HEALTH_SOC: list[float] = [20, 80]
        
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