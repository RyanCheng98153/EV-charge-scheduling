from src.vehicle import Vehicle, VehicleState
from src.charger import Charger, ChargerState
from src.schedule import TaskSchedule, TravelSchedule, ChargeSchedule


class Scheduler():
    def __init__(self, _peak_hour: tuple, _peak_power_price: float, _offpeak_power_price: float):
        self.vehicles: dict[str, Vehicle] = {}
        self.chargers: dict[str, Charger] = {}
        
        Charger.PEAK_HOUR = _peak_hour
        Charger.PEAK_POWER_PRICE = _peak_power_price
        Charger.OFFPEAK_POWER_PRICE = _offpeak_power_price
        
        self.TIMESLOTS = 672
        # self.schedule_table: list[TravelSchedule] = []
        self.schedule_table: list[TaskSchedule] = []
        self.travel_table: list[TravelSchedule] = []
        self.charge_table: list[ChargeSchedule] = []
    
    def reset(self):
        for vehicle in self.vehicles.values():
            vehicle.reset()  # 重置每台車的狀態（e.g., SoC、狀態等）
        for charger in self.chargers.values():
            charger.reset()  # 重置充電站的狀態（e.g., 是否有車連接等）
        self.travel_table = []
        self.charge_table = []

    
    def getCost(self):
        # print(f"TEST: {sum([charge.DEGRADE_COST for charge in self.charge_table])}")
        return sum([charge.COST for charge in self.charge_table]) + sum([charge.DEGRADE_COST for charge in self.charge_table])
    
    def simulate(self):
        for curTime in range(0, self.TIMESLOTS-1):
            # 1. 先看車子是否結束流程 -> 退化 cost 
            
            for schedule in self.travel_table:
                if schedule.finished:
                    continue
                
                if schedule.END_TIME == curTime:
                    vehicle = self.vehicles[schedule.VEHICLE_ID]
                    vehicle.returnStation()
                    schedule.finished = True
            
            # 2. 看目前車子是否充到 HSoC_max -> 斷電 -> 電費 cost

            for charger in self.chargers.values():
                if charger.vehicle == None:
                    continue
                # if charger.vehicle.soc >= charger.vehicle.HEALTH_SOC[1]:
                if charger.vehicle.soc >= 100:
                    v_id, startT, endT, charge_energy, charge_cost, degrade_cost = charger.unplugVehicle(curTime)
                    if startT != endT:
                        self.charge_table.append(ChargeSchedule(startT, endT, 
                                                                v_id, charger.ID, 
                                                                charge_energy, charge_cost, degrade_cost))
                
            # 3 先看車子是否要出發 -> 先發車 -> 斷電，如果無法完成下一班次 -> 模擬結束 
            
            for schedule in self.schedule_table:
                if schedule.START_TIME != curTime:
                    continue
                
                available_vehicles = [
                    vehicle for vehicle in self.vehicles.values() 
                    if vehicle.state == VehicleState.IDLE
                ] + [
                    vehicle for vehicle in self.vehicles.values() 
                    if vehicle.state == VehicleState.CHARGING
                ]
                
                available_vehicles = [ 
                    vehicle for vehicle in available_vehicles 
                    if vehicle.remain_energy > vehicle.getTravelEnergy(schedule.DISTANCE) 
                ]
                
                if len(available_vehicles) == 0:
                    # raise ValueError(f"Time ({curTime}) no available vehicle for task: [ {schedule} ]")
                    vehicle = max(self.vehicles.values(), key=lambda vehicle: vehicle.remain_energy)
                else:
                    vehicle = available_vehicles[0]
                
                if vehicle.state == VehicleState.CHARGING:
                    charger = self.chargers[vehicle.charger_id]
                    v_id, startT, endT, charge_energy, charge_cost, degrade_cost = charger.unplugVehicle(curTime)
                    if startT != endT:
                        self.charge_table.append(ChargeSchedule(startT, endT, 
                                                                v_id, charger.ID, 
                                                                charge_energy, charge_cost, degrade_cost))
                
                vehicle.travel(schedule.DISTANCE, curTime)
                self.travel_table.append(TravelSchedule(schedule.START_TIME, schedule.END_TIME, vehicle.ID, schedule.DISTANCE))
                
            # 4. 充電策略的時間 -> plugVehicle (Y/N) -> 更新充電狀態
            
            for vehicle in self.vehicles.values():
                # only idle vehicle can be charged
                if vehicle.state != VehicleState.IDLE:
                    continue
                if vehicle.soc >= 100:
                    continue
                # vehicle.soc > vehicle.HEALTH_SOC[1] means vehicle is healthy enough, no need to charge
                if vehicle.soc > vehicle.HEALTH_SOC[1]:
                   continue
                for charger in self.chargers.values():
                    # check if charger is available
                    if charger.state != ChargerState.IDLE:
                        continue
                    if not vehicle.VEHICLE_TYPE in charger.charge_type.SERVED_VEHICLES:
                        continue
                    
                    charger.plugVehicle(vehicle, curTime)
                    break
            
            # 5. 執行充電動作
            
            for vehicle in self.vehicles.values():
                if vehicle.state != VehicleState.CHARGING:
                    continue
                self.chargers[vehicle.charger_id].charging()
    
    def simulate_step(self, curTime: int):
        # Step 1: 更新車輛的行程結束邏輯, 回到站點 -> 退化 cost
        for schedule in self.travel_table:
            if schedule.finished:
                continue
            if schedule.END_TIME == curTime:
                vehicle = self.vehicles[schedule.VEHICLE_ID]
                vehicle.returnStation()
                schedule.finished = True
        
        # Step 2: 檢查充電完成的車輛, 充到 HSoC_max, 斷電 -> 電費 cost
        for charger in self.chargers.values():
            if charger.vehicle is None:
                continue
            # if charger.vehicle.soc >= charger.vehicle.HEALTH_SOC[1]:
            
            # 車輛充滿電後, 斷電
            if charger.vehicle.soc >= 100:
                v_id, startT, endT, charge_energy, charge_cost, degrade_cost = charger.unplugVehicle(curTime)
                if startT != endT:
                    self.charge_table.append(ChargeSchedule(startT, endT, 
                                                            v_id, charger.ID, 
                                                            charge_energy, charge_cost, degrade_cost))
        # Step 3: 更新車輛發車邏輯 -> 斷電, 先發車
        # : 如果無法完成下一班次 -> 模擬結束 
        for schedule in self.schedule_table:
            if schedule.START_TIME != curTime:
                continue
            
            # 篩選符合條件的車輛 idle 跟 charging 的車輛
            available_vehicles = [
                vehicle for vehicle in self.vehicles.values() 
                if vehicle.state in {VehicleState.IDLE, VehicleState.CHARGING} 
                and vehicle.remain_energy > vehicle.getTravelEnergy(schedule.DISTANCE)
            ]
            
            # 依照車輛狀態排序, 先發 idle 車輛
            available_vehicles.sort(key=lambda v: v.state == VehicleState.CHARGING)
            
            # 如果沒有符合條件的車輛, 選擇剩餘電量最多的車輛
            if len(available_vehicles) == 0:
                # vehicle = max(self.vehicles.values(), key=lambda vehicle: vehicle.remain_energy)
                raise ValueError(f"Time ({curTime}) no available vehicle for task: [ {schedule} ]")
            vehicle = available_vehicles[0]
            
            if vehicle.state == VehicleState.CHARGING:
                charger = self.chargers[vehicle.charger_id]
                v_id, startT, endT, charge_energy, charge_cost, degrade_cost = charger.unplugVehicle(curTime)
                if startT != endT:
                    self.charge_table.append(ChargeSchedule(startT, endT, 
                                                                v_id, charger.ID, 
                                                                charge_energy, charge_cost, degrade_cost))

            vehicle.travel(schedule.DISTANCE, curTime)
            self.travel_table.append(TravelSchedule(schedule.START_TIME, schedule.END_TIME, vehicle.ID, schedule.DISTANCE))
            
        # Step 4: 執行充電邏輯
        for vehicle in self.vehicles.values():
            if vehicle.state in {VehicleState.TRAVEL, VehicleState.CHARGING} or vehicle.soc >= 100:
                continue
            # vehicle.soc > vehicle.HEALTH_SOC[1] means vehicle is healthy enough, no need to charge
            # if vehicle.soc > vehicle.HEALTH_SOC[1]:
            #     continue
            for charger in self.chargers.values():
                # 充電站是否可用 
                if charger.state != ChargerState.IDLE:
                    continue
                # 車輛型號是否能被該充電樁服務
                if vehicle.VEHICLE_TYPE not in charger.charge_type.SERVED_VEHICLES:
                    continue
                charger.plugVehicle(vehicle, curTime)
                break
            
        # Step 5: 執行充電動作
        for vehicle in self.vehicles.values():
            if vehicle.state != VehicleState.CHARGING:
                continue
            self.chargers[vehicle.charger_id].charging()
    
    def plug_vehicle(self, vehicle: Vehicle, curTime):
        if vehicle.soc >= 100:
            return
        for charger in self.chargers.values():
            if charger.state == ChargerState.IDLE and vehicle.VEHICLE_TYPE in charger.charge_type.SERVED_VEHICLES:
                charger.plugVehicle(vehicle, curTime)
                break
                
    def unplug_vehicle(self, vehicle: Vehicle, curTime):
        if vehicle.state == VehicleState.CHARGING:
            charger = self.chargers[vehicle.charger_id]
            # charger.unplugVehicle(curTime)
            
            v_id, startT, endT, charge_energy, charge_cost, degrade_cost = charger.unplugVehicle(curTime)
            if startT != endT:
                self.charge_table.append(ChargeSchedule(startT, endT, 
                                                        v_id, charger.ID, 
                                                        charge_energy, charge_cost, degrade_cost))
                
            
    def getResult(self):
        return {
            "TotalCost": round(self.getCost(), 4),
            "travel_table": [ self.format_travel(s) for s in self.travel_table ],
            "charge_table": [ self.format_charge(s) for s in self.charge_table]
        }
        
    def format_travel(self, s: TravelSchedule) -> dict:
        return {
            "Start":    s.START_TIME,
            "End":      s.END_TIME,
            "Vehicle":  s.VEHICLE_ID,
            "Distance": s.DISTANCE
        }
        
    def format_charge(self, s: ChargeSchedule) -> dict:
        return {
            "Start":    s.START_TIME,
            "End":      s.END_TIME,
            "Vehicle":  s.VEHICLE_ID,
            "Charger":  s.CHARGER_ID,
            "Energy":   round(s.ENERGY, 4),
            "Cost":     round(s.COST, 4),
            "D-Cost":   round(s.DEGRADE_COST, 4)
        }


    def setVehicles(self, _vehicles: list[Vehicle] ):
        self.vehicles = {vehicle.ID: vehicle for vehicle in _vehicles}
    
    
    def setVehicles(self, _vehicles: list[Vehicle] ):
        self.vehicles = {vehicle.ID: vehicle for vehicle in _vehicles}
        # self.vehicles = _vehicles
        
    def setchargers(self, _chargers: list[Charger] ):
        self.chargers = {charger.ID: charger for charger in _chargers}
        # self.chargers = _chargers
        
    def setSchedules(self, _schedule_table: list[TravelSchedule]):
        self.schedule_table = _schedule_table
        self.schedule_table = sorted(self.schedule_table, key=lambda schedule: schedule.END_TIME, reverse=False)
        self.schedule_table = sorted(self.schedule_table, key=lambda schedule: schedule.START_TIME, reverse=False)
        