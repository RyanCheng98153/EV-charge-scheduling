# EV-charge-scheduling
It is a repository for optimizing Electric Vehicle (EVs) charging scheduling problem
## Introduction
EV charging scheduling is a sub-problem of job scheduling problem, also known as a NP problem.
## Method
- Heuristic Algorithm
- Greedy-like Algorithm

# Requirements
### Simulation
- No Requirement
### Visualize
```
pip install matplotlib
```

# Usage
```
python main.py
```

## Simulation steps concept
```coffee
    def simulate(self):
        finish_action = 0
        
        # schedule vehicle startT endT distance
        for time in range(0, self.TIMESLOTS-1):
            1. 先看車子是否結束流程 -> 退化 cost 
            2. 看充電樁是否結束流程 -> 電費 cost 
            3. 先看車子是否要出發 -> 先發車 -> 斷電，如果無法完成下一班次 -> 模擬結束 
            4. 充電策略的時間 
            - 車1 : 樁1
            -   符合 constraint 的最好充電量 (greedy)
            -   先充到 HSoC_max (80%) -> 斷電 (先看一個班次)
            -   先發車 -> 斷電，如果無法完成下一班次 -> 模擬結束
            - - 班表:
                    尖峰1(6~10): 每 10~15 分鐘 一班車
                    尖峰2(15~19): 每 10~15 分鐘 一班車
                    離峰 ~ 末班車：剩下時間 每 15~20 分鐘 一班車
                    以 236 公車 資料參考
                規格：
                - 參考欣興客運
                - 電費: 尖峰
```

### bus 236 simulation info
```coffee
[ === 模擬參數 === ]
# Electricity: Peak Hour: 16:00 ~ 22:00, 
# : Peak Power Price: 每度電 10.7 元,
# : Offpeak Power Price: 每度電 2.62 元

# 車種: 華德低地板公車, 成運公車
# : 華德低地板公車: 13,000kg, 電池容量: 282,000Wh
# : 成運公車: 16,300kg, 電池容量: 109,000Wh

# 充電樁: 華德雙槍充電樁, 成運三槍充電樁
# 華德雙槍充電樁: 價值 1,300,000 元, 
# : 充電功率: 120,000W (120kW), 1 小時充電 120,000Wh, 
# : 服務車種: 華德低地板公車
# 成運三槍充電樁: 價值 1,200,000 元,
# : 充電功率: 330,000W (330kW), 1 小時充電 330,000Wh,
# : 服務車種: 成運公車

# 欣興客運總車數: 華德低地板公車 56 輛, 成運公車 38 輛
# 欣興客運總充電樁數: 華德車樁比 1:1, 成運車樁比 4:1

[ === 本次模擬 === ]
# Vehicle 數量:
# 236 客運: 華德低地板公車 13 輛

# Vehicle 參數:
# : HEALTH_SOC = [0.2, 0.8] (soc: 20%~80%)
# : ALPHA = 0.6 (行使功耗公式: Energy = ALPHA * 車重(公斤) * 行駛距離(公里))

# Charger 數量:
# 236 客運 (華德低地板公車) => 車數 : 充電樁數 = 1 : 1 => 13台車 : 13台充電樁

[ === Schedule 資訊 === ]
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
)
```

### Visualize
- visualize the greedy method
  - `python ./visual.py ./result.json`
- visualize the genetic method
  - `python .\visual.py .\results\result_10.json 0`
- [file]: Store the figure file