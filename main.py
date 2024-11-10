from src.scheduler import Scheduler
from src.schedule import TaskSchedule, TravelSchedule, TaskFactory, RealTime
from src.vehicle import Vehicle, VehicleType
from src.charger import Charger, ChargerType

def main():
    
    # alpha = 0.5
    
    # Electricity: Peak Hour: 16:00 ~ 22:00, 
    # : Peak Power Price: 每度電 10.7 元,
    # : Offpeak Power Price: 每度電 2.62 元
    scheduler = Scheduler(_peak_hour=(16, 22), _peak_power_price=10.7, _offpeak_power_price=2.62)
    
    # 車種: 華德低地板公車, 成運公車
    # : 華德低地板公車: 13,000kg, 電池容量: 282,000Wh
    # : 成運公車: 16,300kg, 電池容量: 109,000Wh
    vehicleTypes : dict[str, VehicleType] = {
        item.name: item for item in [
            VehicleType(_name="華德低地板公車", _value=10500000, _weight=13000, _battery=282000),
            VehicleType(_name="成運公車", _value=10500000, _weight=16300, _battery=109000),
        ]}
    
    # 充電樁: 華德雙槍充電樁, 成運三槍充電樁
    # 華德雙槍充電樁: 價值 1,300,000 元, 
    # : 充電功率: 120,000W (120kW), 1 小時充電 120,000Wh, 
    # : 服務車種: 華德低地板公車
    # 成運三槍充電樁: 價值 1,200,000 元,
    # : 充電功率: 330,000W (330kW), 1 小時充電 330,000Wh,
    # : 服務車種: 成運公車
    chargerTypes : dict[str, ChargerType] = {
        item.name: item for item in [
            ChargerType('華德雙槍充電樁', _value=1300000, _hour_charge_rate=120000, _served_vehicles=[vehicleTypes["華德低地板公車"]]),
            ChargerType('成運三槍充電樁', _value=1200000, _hour_charge_rate=330000, _served_vehicles=[vehicleTypes["成運公車"]])
        ]}

    # 欣興客運總車數: 華德低地板公車 56 輛, 成運公車 38 輛
    # 236 客運: 華德低地板公車 13 輛
    vehicles : list[Vehicle] = [
        Vehicle(f'華德_{i}', vehicleTypes["華德低地板公車"]) for i in range(0, 13)
    ] + [
        Vehicle(f'成運_{i}', vehicleTypes["成運公車"]) for i in range(0, 0)
    ]
    
    # 欣興客運總充電樁數: 華德車樁比 1:1, 成運車樁比 4:1
    # 236 客運 (華德低地板公車) => 車數 : 充電樁數 = 1 : 1 => 13台車 : 13台充電樁
    chargers : list[Charger] = [
        Charger(f'華德充電樁_{i}', chargerTypes["華德雙槍充電樁"]) for i in range(0, 13)
    ] + [
        Charger(f'成運充電樁_{i}', chargerTypes["成運三槍充電樁"]) for i in range(0, 13)
    ]
    
    scheduler.setVehicles(vehicles)
    scheduler.setchargers(chargers)
    
    
    # 客制化出發排程
    # scheduler.setSchedules([
    #     TaskSchedule(0,      1,      vehicleTypes['華德低地板公車'], 10),
    #     TaskSchedule(2,      3,      vehicleTypes['華德低地板公車'], 10),
    #     TaskSchedule(4,      5,      vehicleTypes['華德低地板公車'], 10),
    # ])
    
    # 使用 Task Factory 生成 尖峰 15 分一班，離峰 30 分一班的排程
    scheduler.setSchedules( 
        TaskFactory.generate(
            vehicle_type=vehicleTypes["華德低地板公車"],
            distance=18, # 旅程 18 公里
            travel_time=RealTime(1, 30 ), # 旅程 1 小時 30 分鐘
            first_run=RealTime(5, 30), # 首班 5:30 開始
            last_run=RealTime(23, 15), # 末班 23:15 結束
            frequency=RealTime(0, 30), # 離峰 30 分一班
            rush_hour=[ # 尖峰時段 7:00 ~ 9:00, 17:00 ~ 19:30
                (RealTime(7, 0), RealTime(9, 0)), 
                (RealTime(17, 0), RealTime(19, 30))
            ],
            rush_freq=RealTime(0, 15), # 尖峰 15 分一班
            weekdays=[0], # 0: Monday, 1: Tuesday, 2: Wednesday, 3: Thursday, 4: Friday, 5: Saturday, 6: Sunday
        ))
    
    
    def printSchedule():
        print("[ === Travel Table === ]")
        for schedule in scheduler.travel_table:
            print(schedule)
        print()
        
        print("[ === Charge Table === ]")
        for schedule in scheduler.charge_table:
            print(schedule)
        print()
        
        print("[ === Vehicle Table === ]")
        for vehicle in scheduler.vehicles.values():
            print(vehicle)
        print()
    
    print("[ Simulate Started ... ]")
    print()
    # scheduler.simulate()
    
    try :
        scheduler.simulate()
        
        printSchedule()
        
        print("[ End Successfully ... ]")   
        print()
    
    except Exception as e:
        
        printSchedule()
        
        print("[ Error Occurred ... ]: ", e)
        print("[ Progress Terminate ... ]")
        # exit()
    
    print(f"Total Cost: {scheduler.getCost()}")
    
if __name__ == "__main__":
    main()