class TravelSchedule:
    def __init__(self,
                 _start_time: int,
                 _end_time: int,
                 _vehicle_id: str,
                 _distance: float
                 ) -> None:
        self.START_TIME = _start_time
        self.END_TIME = _end_time
        self.VEHICLE_ID = _vehicle_id
        self.DISTANCE = _distance
        self.finished: bool = False
        pass

class TravelScheduleTable:
    def __init__(self):
        pass
    
    def generate():
        pass

        
class ChargeSchedule:
    def __init__(self,
                 _start_time: int,
                _end_time: int,
                 _vehicle_id: str,
                 _charger_id: str,
                 _energy: float,
                 _cost: float
                 ) -> None:
        self.START_TIME = _start_time
        self.END_TIME = _end_time
        self.VEHICLE_ID = _vehicle_id
        self.CHARGER_ID = _charger_id
        self.CHARGE_TIME = _end_time - _start_time
        self.ENERGY = _energy
        self.COST = _cost
        pass
    
    def __repr__(self):
        return f"Start: {self.START_TIME: <4} End: {self.END_TIME: <4} ChargeTime: {self.CHARGE_TIME: <4} Vehicle: {self.VEHICLE_ID: <6} Charger: {self.CHARGER_ID: <6} Energy: {self.ENERGY: >8} (Whr) Cost: {self.COST:>8.2f} (元)"