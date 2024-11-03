from src.scheduler import Scheduler
from src.schedule import TravelSchedule
from src.vehicle import Vehicle, VehicleType
from src.charger import Charger, ChargerType

def main():
    # print("Start")
    scheduler = Scheduler(_peak_hour=(16, 22), _peak_power_price=10.7, _offpeak_power_price=2.62)
    
    # # Vehicle Battery: 282,000Wh, 109000Wh 單位: 瓦小時
    # vehicleTypes : dict[str, VehicleType] = {
    #     "華德低地板公車": VehicleType(_name="華德低地板公車", _value=10500000, _weight=13000, _battery=282000),
    #     "成運公車":     VehicleType(_name="成運公車", _value=10500000, _weight=16300, _battery=109000),
    #     }
    
    # Vehicle Battery: 282,000Wh, 109000Wh 單位: 瓦小時
    vehicleTypes : dict[str, VehicleType] = {
        item.name: item for item in [
            VehicleType(_name="華德低地板公車", _value=10500000, _weight=13000, _battery=282000),
            VehicleType(_name="成運公車", _value=10500000, _weight=16300, _battery=109000),
        ]}
    
    # # ChargeRate: 120,000W, 330,000W 單位: 瓦小時
    # chargerTypes : dict[ChargerType] = {
    #     "華德雙槍充電樁": ChargerType('華德雙槍充電樁', _value=1300000, _charge_rate=120000, _served_vehicles=[vehicleTypes["華德低地板公車"]]),
    #     "成運三槍充電樁": ChargerType('成運三槍充電樁', _value=1200000, _charge_rate=330000, _served_vehicles=[vehicleTypes["成運汽車"]]),
    # }
    
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
    
    # print("Vehicles:")
    # for vehicle in vehicles:
    #     vehicle.printVehicleInfo()
    # print("Vehicles End")
    
    # 欣興客運總充電樁數: 華德低地板公車 56 輛, 成運公車 38 輛
    # 236 客運 (華德低地板公車) => 車數 : 充電樁數 = 1 : 1 
    chargers : list[Charger] = [
        Charger(f'華德充電樁_{i}', chargerTypes["華德雙槍充電樁"]) for i in range(0, 1)
    ] + [
        Charger(f'成運充電樁_{i}', chargerTypes["成運三槍充電樁"]) for i in range(0, 13)
    ]
    
    scheduler.setVehicles(vehicles)
    scheduler.setchargers(chargers)
    
    # scheduler.setVehicles([
    #     Vehicle('v1', vehicleTypes["華德低地板公車"], 100000, 1000, 100000 ),
    #     Vehicle('v2', vehicleTypes["華德低地板公車"], 20000, 200, 20000 ),
    #     Vehicle('v3', vehicleTypes["成運汽車"], 30000, 300, 30000 ),
    #     Vehicle('v4', vehicleTypes["成運汽車"], 40000, 400, 40000 ),
    #     Vehicle('v5', vehicleTypes["成運汽車"], 50000, 500, 50000 ),
    # ])
    # scheduler.setchargers([
    #     Charger('c1', chargerTypes["華德雙槍充電樁"], 100000, 10),
    #     Charger('c2', chargerTypes["華德雙槍充電樁"], 200000, 20),
    #     Charger('c3', chargerTypes['成運三槍充電樁'], 300000, 30),
    # ])
    
    
    scheduler.setSchedules([
        TravelSchedule(0, 1, '華德_1', 10),
        TravelSchedule(2, 3, '華德_1', 10),
        TravelSchedule(4, 5, '華德_1', 10),
        TravelSchedule(7, 8, '華德_1', 10),
        TravelSchedule(10, 11, '華德_1', 10),
        TravelSchedule(12, 13, '華德_1', 10),
        TravelSchedule(70, 110, '華德_1', 10),
        TravelSchedule(20, 65, '華德_2', 12),
        TravelSchedule(0, 40, '華德_3', 20),
        TravelSchedule(60, 75, '華德_3', 8),
        TravelSchedule(90, 105, '華德_3', 6),
        TravelSchedule(0, 20, '華德_4', 6),
        TravelSchedule(40, 80, '華德_4', 15),
        TravelSchedule(20, 70, '華德_4', 25),
    ])
    
    # scheduler.setSchedules([
    #     TravelSchedule(0, 1,    vehicleTypes["華德低地板公車"], 10),
    #     TravelSchedule(2, 3,    vehicleTypes["華德低地板公車"], 10),
    #     TravelSchedule(4, 5,    vehicleTypes["華德低地板公車"], 10),
    #     TravelSchedule(7, 8,    vehicleTypes["華德低地板公車"], 10),
    #     TravelSchedule(10, 11,  vehicleTypes["華德低地板公車"], 10),
    #     TravelSchedule(12, 13,  vehicleTypes["華德低地板公車"], 10),
    #     TravelSchedule(70, 110, vehicleTypes["華德低地板公車"], 10),
    #     TravelSchedule(20, 65,  vehicleTypes["華德低地板公車"], 12),
    #     TravelSchedule(0, 40,   vehicleTypes["華德低地板公車"], 20),
    #     TravelSchedule(60, 75,  vehicleTypes["華德低地板公車"], 8),
    #     TravelSchedule(90, 105, vehicleTypes["華德低地板公車"], 6),
    #     TravelSchedule(0, 20,   vehicleTypes["華德低地板公車"], 6),
    #     TravelSchedule(40, 80,  vehicleTypes["華德低地板公車"], 15),
    #     TravelSchedule(20, 70,  vehicleTypes["華德低地板公車"], 25),
    # ])
    
    print("[ Simulate Started ... ]")
    
    # scheduler.simulate()
    
    try :
        scheduler.simulate()
    except Exception as e:
        print("[ Error Occurred ... ]: ", e)
        print("[ Progress Terminate ... ]")
        exit()
    
    for schedule in scheduler.charge_table:
        print(schedule)
    
    print("[ End Successfully ... ]")   
    print("Next Step: Change Vehicle from ID to Type")    
    
if __name__ == "__main__":
    main()