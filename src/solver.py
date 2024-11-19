import random
from src.scheduler import Scheduler, VehicleState

class Solver:
    def __init__(self, scheduler: Scheduler, population_size: int, generations: int, mutation_rate: float):
        self.scheduler = scheduler
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = []  # 每個基因代表充電策略的編碼
        self.best_solution = None
        self.best_fitness = float('inf')
    
    def initialize_population(self):
        """初始化族群，每個個體的基因代表每個時間、每台車的充電策略"""
        self.population = [
            [
                {
                    vehicle_id: random.choice([True, False])  # True: 充電, False: 不充電
                    for vehicle_id in self.scheduler.vehicles
                }
                for _ in range(self.scheduler.TIMESLOTS)
            ]
            for _ in range(self.population_size)
        ]
    
    def fitness(self, genes):
        """計算適應值（總能量消耗）"""
        self.scheduler.reset()  # 重置模擬環境
        try:
            for curTime, decisions in enumerate(genes):
                for vehicle_id, should_charge in decisions.items():
                    vehicle = self.scheduler.vehicles[vehicle_id]
                    if vehicle.state == VehicleState.IDLE and should_charge:
                        self.scheduler.plug_vehicle(vehicle, curTime)
                    elif vehicle.state == VehicleState.CHARGING and not should_charge:
                        self.scheduler.unplug_vehicle(vehicle, curTime)
                self.scheduler.simulate_step(curTime)  # 執行單步模擬
            return self.scheduler.getCost()
        except Exception as e:
            # 捕獲例外，返回當前累積的能量成本作為適應值
            # print(f"Exception during simulation: {e}")
            return self.scheduler.getCost()
    
    def select_best(self):
        """選擇族群中適應值最好的個體"""
        best_individual = None
        best_fitness = float('inf')
        for genes in self.population:
            current_fitness = self.fitness(genes)
            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best_individual = genes
        return best_individual, best_fitness
    
    def mutate(self, genes):
        """隨機突變，變動某些基因（充電策略）"""
        for time in range(self.scheduler.TIMESLOTS):
            if random.random() < self.mutation_rate:
                vehicle_id = random.choice(list(self.scheduler.vehicles.keys()))
                genes[time][vehicle_id] = not genes[time][vehicle_id]
        return genes
    
    def solve(self):
        """執行基因演算法主流程"""
        self.initialize_population()
        
        for generation in range(self.generations):
            # 更新族群：突變生成新族群
            new_population = []
            for genes in self.population:
                mutated_genes = self.mutate(genes.copy())
                new_population.append(mutated_genes)
            self.population = new_population
            
            # 計算最佳解
            try:
                current_best_solution, current_best_fitness = self.select_best()
                if current_best_fitness < self.best_fitness:
                    self.best_fitness = current_best_fitness
                    self.best_solution = current_best_solution
            except Exception as e:
                print(f"Error during selection: {e}")
                continue
            
            print(f"Generation {generation+1}/{self.generations}: Best Fitness = {self.best_fitness}")
        
        return self.best_solution, self.best_fitness
