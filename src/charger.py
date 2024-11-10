from src.vehicle import Vehicle, VehicleType
from enum import Enum

class ChargerState(Enum):
    IDLE = 0
    CHARGING = 1

class ChargerType():
    def __init__(self, _name:str , _value:float, _hour_charge_rate:float, _served_vehicles: list[VehicleType] = None):
        self.name: str = _name
        self.value: float = _value
        self.hour_charge_rate: float = _hour_charge_rate
        self.SERVED_VEHICLES: list[VehicleType] = _served_vehicles
        
    def __repr__(self):
        return f"ChargerType: {self.name: <15} Value: {self.value: <8} Charge Rate: {self.charge_rate: <8}"

class Charger:
    
    PEAK_HOUR: tuple[int] = (None, None)
    
    PEAK_POWER_PRICE: float = None
    OFFPEAK_POWER_PRICE: float = None
    
    def __init__(self, 
                 _id:                   str, 
                 _charger_type:         ChargerType = None,
                 _charger_value:        float = None, 
                 _charge_rate_per_hour: float = None
                 ) -> None:
        # Constant informations
        self.ID: str = _id
        self.charge_type: ChargerType = _charger_type
        # Use chargerType's default value if not given in constructor
        self.CHARGER_VALUE: float           = _charger_value        if _charger_value        != None else _charger_type.value
        # timeslot (15分鐘) 充電速度 = 小時充電速度 / 4
        hour_charge_rate: float             = _charge_rate_per_hour if _charge_rate_per_hour != None else _charger_type.hour_charge_rate
        self.CHARGE_RATE_PER_TIME: float    = hour_charge_rate / 4
        self.SERVED_VEHICLES: list[VehicleType] = _charger_type.SERVED_VEHICLES
        
        # member variables
        self.vehicle: Vehicle = None
        self.state = ChargerState.IDLE
        
        self.start_time: int = 0
        self.idle_time: int = 0
        
        self.charge_time: int = 0
        self.charge_energy: float = 0.0
        self.charge_cost: float = 0.0
        pass
    
    def __repr__(self):
        return f"Charger: {self.ID: <8} State: {self.state.name: <10} IdleTime: {self.idle_time: <8} Vehicle: {'None' if self.vehicle == None else self.vehicle.ID: <8} ChargeRate: {self.CHARGE_RATE_PER_TIME}"
    
    def plugVehicle(self, _vehicle: Vehicle, _start_time: int) -> None:
        self.state = ChargerState.CHARGING
        self.vehicle = _vehicle
        self.start_time = _start_time
        self.vehicle.plugVehicle(_start_time, self.ID)
        # Printing...
        # self.vehicle.printVehicleInfo()
        
    def charging(self) -> None:
        self.vehicle.chargeBattery(self.CHARGE_RATE_PER_TIME)
    
    def unplugVehicle(self, _finish_time: int) -> tuple[str, int, int, float, float]:
        self.state = ChargerState.IDLE
        self.vehicle.unplugVehicle(_finish_time)
        
        v_id = self.vehicle.ID
        charge_time = _finish_time - self.start_time
        charge_energy = charge_time * self.CHARGE_RATE_PER_TIME
        charge_cost = self.__func1_getChargeCost(self.start_time, _finish_time-self.start_time)
        
        self.idle_time = _finish_time
        
        self.vehicle = None
        self.charge_time = 0
        self.charge_energy = 0.0
        self.charge_cost = 0.0
        
        return v_id, self.start_time, self.idle_time, charge_energy, charge_cost
    
    # E_t
    def __func1_getChargeCost(self, _start_time: int, _charge_time:int) -> float:
        
        # timeslot: 24 hours = 96 timeslot, 
        # ex: 若 PEAK_HOUR = 16:00 ~ 22:00 => timeslot = 64 ~ 88
        PEAK_HOUR_START, PEAK_HOUR_END = self.PEAK_HOUR[0] * 4, self.PEAK_HOUR[1] * 4
        
        # timeslot: 24 hours = 96 timeslot, 9 hours = 36 timeslot
        peak_time = _charge_time // 96 * 60
        offpeak_time = _charge_time // 96 * 36
        
        # 計算結束時間，並模擬24小時（96個timeslot）循環
        end_time = (_start_time + _charge_time) % 96
        
        # 情況 1：不跨午夜
        if _start_time < end_time:
            # 尖峰時間的重疊部分: 若 start_time 或 end_time 在尖峰時段外，則選 Peak Hour 的 START 或 END 作為計算
            peak_time = max(0, min(end_time, PEAK_HOUR_END) - max(_start_time, PEAK_HOUR_START))
        else:  # 情況 2：跨午夜
            # 當天的尖峰時間重疊部分: 若 start_time 在尖峰時段外，則選 Peak Hour 的 START 作為計算
            peak_time_day1 = max(0, PEAK_HOUR_END - max(_start_time, PEAK_HOUR_START))
            # 次日的尖峰時間重疊部分: 若 end_time 在尖峰時段外，則選 Peak Hour 的 END 作為計算
            peak_time_day2 = max(0, min(end_time, PEAK_HOUR_END) - PEAK_HOUR_START)
            # 總尖峰時間
            peak_time = peak_time_day1 + peak_time_day2
        
        # 離峰時間為充電總時長減去尖峰時長
        offpeak_time = _charge_time - peak_time
        
        # time * charge_rate_per_time = 多少瓦 
        # 1000 瓦小時 = 度電
        peak_time_energy_cost       = peak_time * self.CHARGE_RATE_PER_TIME / 1000 * self.PEAK_POWER_PRICE
        offpeak_time_energy_cost = offpeak_time * self.CHARGE_RATE_PER_TIME / 1000 * self.OFFPEAK_POWER_PRICE
        
        # print(f"peak({peak_time}): {peak_time_energy_cost:.1f}, offpeak({(offpeak_time)}): {offpeak_time_energy_cost:.1f}, total({_charge_time}): {peak_time_energy_cost + offpeak_time_energy_cost:.1f}")
        return peak_time_energy_cost + offpeak_time_energy_cost
    
    