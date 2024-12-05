from src.vehicle import VehicleType
class TaskSchedule:
    def __init__(self,
                 _start_time: int,
                 _end_time: int,
                 _vehicle_type: VehicleType,
                 _distance: float
                 ) -> None:
        self.START_TIME = _start_time
        self.END_TIME = _end_time
        self.VEHICLE_TYPE = _vehicle_type
        self.DISTANCE = _distance
        pass
    def __repr__(self):
        return f"Start: {self.START_TIME: <3} End: {self.END_TIME: <3} VehicleType: {self.VEHICLE_TYPE.name: <10} Distance: {self.DISTANCE: >3} (km)"
        pass

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
    
    # overloading constructor by given TaskSchedule as parameter
    @classmethod
    def byTask(cls,
                 _vehicle_id: str,
                 _task: TaskSchedule
                 ) -> None:
        
        return cls(_task.START_TIME, _task.END_TIME, _vehicle_id, _task.DISTANCE)
    
    def __repr__(self):
        return f"Start: {self.START_TIME: <4} End: {self.END_TIME: <4} Vehicle: {self.VEHICLE_ID: <6} Distance: {self.DISTANCE: >3} (km)"


class RealTime:
    HOUR_TIMESLOT:int = 4
    MINUTE_TIMESLOT:int = 15
    DAY_TIMESLOT:int = 24 * HOUR_TIMESLOT
    
    def __init__(self, _hour:int, _minute:int) -> None:
        self.Hour = _hour
        self.Minute = _minute
        pass
    
    def getTimeslot(self) -> int:
        return self.Hour * RealTime.HOUR_TIMESLOT + self.Minute // RealTime.MINUTE_TIMESLOT

class TaskFactory:
    def __init__(self):
        pass
    
    @staticmethod
    def generate(vehicle_type: VehicleType, 
                 distance: float, 
                 travel_time: RealTime,
                 first_run: RealTime, 
                 last_run: RealTime, 
                 frequency: RealTime,
                 weekdays: list[int] = [0, 1, 2, 3, 4, 5, 6],
                 rush_hour: list[tuple[RealTime, RealTime]] = [
                     (RealTime(0, 0), RealTime(0, 0)), 
                    ],
                 rush_freq: RealTime = RealTime(0, 0)
                 ) -> TravelSchedule:
        
        task_list:list[TaskSchedule] = []
        
        for day in weekdays:
            # Generate TaskSchedule
            day_time    = day * RealTime.DAY_TIMESLOT
            cur_time    = day_time + first_run.getTimeslot()
            end_time    = day_time + last_run.getTimeslot()
            
            freq_time   = frequency.getTimeslot()
            duration    = travel_time.getTimeslot()
            
            rush_time = [ (day_time + rush[0].getTimeslot(), day_time + rush[1].getTimeslot()) for rush in rush_hour ]
            rush_freq_time = rush_freq.getTimeslot()
            

            while cur_time < end_time:
                task_list.append(TaskSchedule(cur_time, 
                                            cur_time + duration, 
                                            vehicle_type, 
                                            distance
                                            ))
                
                is_rush_hour = False
                # check if current time is in rush hour
                for r_start, r_end in rush_time:
                    if cur_time >= r_start and cur_time <= r_end:
                        cur_time += rush_freq_time
                        is_rush_hour = True
                        break
                
                if not is_rush_hour:
                    cur_time += freq_time
                    
                
        return task_list

        
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