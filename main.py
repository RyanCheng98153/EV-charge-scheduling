from src.scheduler import Scheduler
from src.schedule import TaskSchedule, TravelSchedule, TaskFactory, RealTime
from src.vehicle import Vehicle, VehicleType
from src.charger import Charger, ChargerType

def main():
    
    # Electricity: Peak Hour: 16:00 ~ 22:00, Peak Power Price: 10.7, Offpeak Power Price: 2.62
    scheduler = Scheduler(_peak_hour=(16, 22), _peak_power_price=10.7, _offpeak_power_price=2.62)
    
    # Vehicle Battery: 282,000Wh, 109000Wh 單位: 瓦小時
    vehicleTypes : dict[str, VehicleType] = {
        item.name: item for item in [
            VehicleType(_name="華德低地板公車", _value=10500000, _weight=13000, _battery=282000),
            VehicleType(_name="成運公車", _value=10500000, _weight=16300, _battery=109000),
        ]}
    
    # ChargeRate: 120,000W, 330,000W 單位: 瓦小時
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
    
    # 欣興客運總充電樁數: 華德低地板公車 56 輛, 成運公車 38 輛
    # 236 客運 (華德低地板公車) => 車數 : 充電樁數 = 1 : 1 
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
    
    scheduler.setSchedules( 
        TaskFactory.generate(
            vehicle_type=vehicleTypes["華德低地板公車"], 
            distance=18,
            travel_time=RealTime(1, 30 ),
            first_run=RealTime(5, 30),
            last_run=RealTime(23, 15),
            frequency=RealTime(0, 30),
            rush_hour=[
                (RealTime(7, 0), RealTime(9, 0)), 
                (RealTime(17, 0), RealTime(19, 30))
            ],
            rush_freq=RealTime(0, 15),
            weekdays=[0],
        ))
    
    print("[ Simulate Started ... ]")
    
    # scheduler.simulate()
    
    try :
        scheduler.simulate()
        
        print("[ === Travel Table === ]")
        for schedule in scheduler.travel_table:
            print(schedule)

        print("[ === Charge Table === ]")
        for schedule in scheduler.charge_table:
            print(schedule)

        print("[ === Vehicle Table === ]")
        for vehicle in scheduler.vehicles.values():
            print(vehicle)
        
        print()
        print("[ End Successfully ... ]")   
        print()
    
    except Exception as e:
        print("[ === Travel Table === ]")
        for schedule in scheduler.travel_table:
            print(schedule)

        print("[ === Charge Table === ]")
        for schedule in scheduler.charge_table:
            print(schedule)

        print("[ === Vehicle Table === ]")
        for vehicle in scheduler.vehicles.values():
            print(vehicle)

        print()
        print("[ Error Occurred ... ]: ", e)
        print("[ Progress Terminate ... ]")
        # exit()
    
    print(f"Total Cost: {scheduler.getCost()}")
    
if __name__ == "__main__":
    main()