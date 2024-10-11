# EV-charge-scheduling
It is a repository for optimizing Electric Vehicle (EVs) charging scheduling problem
## Introduction
EV charging scheduling is a sub-problem of job scheduling problem, also known as a NP problem.
## Method
- Heuristic Algorithm
- Greedy-like Algorithm

## Objective Function and Restriction Function
**目標函數: 充電排程之總成本**
$P_1 = \min\{\ \sum\limits_{i=0}^{671}(\ E_t + W_t\ )\ \}$

1. **電池充電成本(日間、夜間計費)**
$ E_t=\sum\limits_{v=1}^{N_{ev}}e_{vt} \cdot Ratio \cdot e_{price} & 9 \leq (t \mod 24) \lt 24
\\ \sum\limits_{v=1}^{N_{ev}}e_{vt} \cdot e_{price} & otherwise
$

2. **電池退化成本**
$ W_t = \sum\limits_{v=1}^{N_{EV}}\mathbb{D} (e_{vt}) \cdot V_v $

7. **電動公車能耗 與車重、行駛距離之關係**
$$ 
EC = \sum\limits_{v=1}^{N_{EV}}\alpha \cdot W_{v} \cdot S_{v}
$$

10. **電池退化率(電池健康、過充情況)**
$\mathbb{D}(e_{vt}) = DCH,  & HCS_{min} \leq SOC_{vt} \leq HCS_{max}
\\ 2~DCH, &  SOC_{vt} \text ~~ {otherwise}
$

11. **健康電池退化率**
$$DCH = DDH = \dfrac{e_{vt}}{CL*(DoD/100\%)*2B}$$


