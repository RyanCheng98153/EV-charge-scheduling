# EV-charge-scheduling
It is a repository for optimizing Electric Vehicle (EVs) charging scheduling problem
## Introduction
EV charging scheduling is a sub-problem of job scheduling problem, also known as a NP problem.
## Method
- Heuristic Algorithm
- Greedy-like Algorithm
- 

## simulation
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