import random
import csv
import time

# Constants for simulation
NUM_ZONES = 4  # Number of irrigation zones
MOISTURE_RANGE = (20, 80)  # Range of moisture values (%)
WATER_FLOW_RANGE = (1, 10)  # Range of water flow values (liters per minute)

# Function to generate random sensor data
def generate_sensor_data():
    moisture_data = [random.randint(*MOISTURE_RANGE) for _ in range(NUM_ZONES)]
    water_flow_data = [random.uniform(*WATER_FLOW_RANGE) for _ in range(NUM_ZONES)]
    return moisture_data, water_flow_data

# Function to update and store sensor data
def update_sensor_data():
    while True:
        # Generate random sensor data
        moisture_data, water_flow_data = generate_sensor_data()

        # Store the updated sensor data in a data file (e.g., CSV)
        with open('sensor_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Zone', 'Moisture', 'Water Flow'])
            for i in range(NUM_ZONES):
                writer.writerow([i+1, moisture_data[i], water_flow_data[i]])

        # Wait for some time before updating again
        time.sleep(3)  # Adjust the sleep time as per your requirements

if __name__ == "__main__":
    update_sensor_data()
