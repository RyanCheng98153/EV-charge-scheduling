from scheduler import Scheduler, Schedule
from src.vehicle import Vehicle
    
def main():
    print("Start")
    scheduler = Scheduler()
    scheduler.setVehicles([
        Vehicle( 0, 1000, 1000 ),
        Vehicle( 1, 2000, 1000 ),
        Vehicle( 2, 2000, 1000 ),
        Vehicle( 3, 3000, 1000 ),
        Vehicle( 4, 3000, 1000 ),
    ])
    
if __name__ == "__main__":
    main()