import matplotlib.pyplot as plt
import json
import sys

# Opening JSON file
with open(sys.argv[1], mode="r", encoding="utf-8") as json_file:
    datas = json.load(json_file)

# Function to convert travel data
def get_travel_dict(travel_item: dict) -> dict:
    # Extract the base name of the vehicle (e.g., '華德' from '華德_0')
    # { "Start": 22, "End": 28, "Vehicle": "華德_0", "Distance": 18 },
    vehicle_name = "HuaDe" + travel_item['Vehicle'].split('_')[1]
    
    # Return a new dictionary with required keys and values
    return {
        'Task': vehicle_name,  # Task is the vehicle name without the suffix
        'Start': travel_item['Start'],  # Start time
        'Finish': travel_item['End']  # End time
    }

# Function to convert travel data
def get_charge_dict(charge_item: dict) -> dict:
    # Extract the base name of the vehicle (e.g., '華德' from '華德_0')
    # { "Start": 0, "End": 0, "Vehicle": "華德_1", "Charger": "華德充電樁_0", "Energy": 0.0, "Cost": 5817.6 },
    # charge_name = "Charger" + charge_item['Charger'].split('_')[1]
    vehicle_name = "HuaDe" + charge_item['Vehicle'].split('_')[1]
    
    # Return a new dictionary with required keys and values
    return {
        'Task': vehicle_name,  # Task is the vehicle name without the suffix
        'Start': charge_item['Start'],  # Start time
        'Finish': charge_item['End']  # End time
    }

if __name__ == '__main__':
    
    if len(sys.argv) >= 3 and sys.argv[2].isdigit():
        num: int = int(sys.argv[2])
        data = datas[0]
    else:
        data = datas
    
    # Convert all travel data and charge data
    travel_data = [get_travel_dict(item) for item in data['travel_table']]
    charge_data = [get_charge_dict(item) for item in data['charge_table']]

    # Create the plot
    fig, ax = plt.subplots(figsize=(108, 6))
    if "day1" in sys.argv[1]:
        fig, ax = plt.subplots(figsize=(12, 6))

    # Plot each task as a bar
    for idx, task in enumerate(travel_data):
        ax.barh(task['Task'], task['Finish'] - task['Start'], left=task['Start'], color='skyblue', edgecolor='black', linewidth=1.5)

    # Plot each task as a bar
    for idx, task in enumerate(charge_data):
        ax.barh(task['Task'], task['Finish'] - task['Start'], left=task['Start'], color='orange', edgecolor='black', linewidth=1.5)

    # Formatting the plot
    ax.set_xlabel('time (30 mins)', fontsize=12)
    ax.set_ylabel('Task', fontsize=12)
    
    total_cost = [data['TotalCost']]
    ax.set_title(f'Bus 236 Travel Table, Total cost: {total_cost}', fontsize=14)

    # Customizing time ticks for better readability
    ticks = range(0, 700, 2)
    if "day1" in sys.argv[1]:
        ticks = range(0, 100, 2)
    # plt.xticks(ticks)  # Adjust this based on your time range
    ax.set_xticks(ticks)
    xlabels = [
        f"<Day {x // 96}>" if x % 96 == 0 else f"{x % 96 // 4:02}:{x % 4 * 15:02}" 
        for x in ticks
    ]
    ax.set_xticklabels(xlabels, minor=False, rotation=45)
    plt.grid(True)

    # Display the plot
    plt.tight_layout()
    
    if (len(sys.argv) == 3 and sys.argv[2] == "file") or (len(sys.argv) == 4 and sys.argv[3] == "file"):
        filename = sys.argv[1].split('/')[-1].split('\\')[-1].split('.')[0]
        
        if sys.argv[2] == "file":
            num = ""
        
        with open(f"./figure/{filename}_fig{num}.png", 'wb') as f:
            fig.savefig(f, bbox_inches="tight", dpi=180)
    else:
        plt.show()