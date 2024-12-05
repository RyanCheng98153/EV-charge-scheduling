import matplotlib.pyplot as plt
import pandas as pd
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
    
    if len(sys.argv) == 3:
        num: int = int(sys.argv[2])
        data = datas[0]
    else:
        data = datas
    
    # Convert all travel data and charge data
    travel_data = [get_travel_dict(item) for item in data['travel_table']]
    charge_data = [get_charge_dict(item) for item in data['charge_table']]

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each task as a bar
    for idx, task in enumerate(travel_data):
        ax.barh(task['Task'], task['Finish'] - task['Start'], left=task['Start'], color='skyblue', edgecolor='black', linewidth=1.5)

    # Plot each task as a bar
    for idx, task in enumerate(charge_data):
        ax.barh(task['Task'], task['Finish'] - task['Start'], left=task['Start'], color='orange', edgecolor='black', linewidth=1.5)

    # Formatting the plot
    ax.set_xlabel('time (15 mins)', fontsize=12)
    ax.set_ylabel('Task', fontsize=12)
    ax.set_title('Bus 236 Travel Table', fontsize=14)

    # Customizing time ticks for better readability
    plt.xticks(range(20, 100, 2))  # Adjust this based on your time range
    plt.grid(True)

    # Display the plot
    plt.tight_layout()
    
    if len(sys.argv) == 3 and sys.argv[2] == "file" and len(sys.argv) == 4 and sys.argv[3] == "file":
        filename = sys.argv[1].split('/')[-1].split('\\')[-1].split('.')[0]
        
        with open(f"./figure/{filename}_fig{num}.png", 'wb') as f:
            fig.savefig(f)
    else:
        plt.show()