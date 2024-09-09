import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import winsound
import cv2
import time
import os


# Constants for simulation
NUM_ZONES = 4  # Number of irrigation zones
MOISTURE_RANGE = (20, 80)  # Range of moisture values (%)
WATER_FLOW_RANGE = (1, 4)  # Range of water flow values (liters per minute)
THRESHOLD = 88  # Threshold for water flow

# Function to generate random sensor data
def generate_sensor_data():
    moisture_data = [random.randint(*MOISTURE_RANGE) for _ in range(NUM_ZONES)]
    return moisture_data

# Function to gradually increase and decrease water flow until threshold is reached
def generate_water_flow_data():
    water_flow_data = []
    with open("water_flow_data.txt", "r") as prev_file, open("flow_decision.txt", "r+") as decision_file:
        flow_decision = decision_file.readline().strip()
        if flow_decision == "increase":
            increasing = True
        elif flow_decision == "decrease":
            increasing = False
        else:
            raise ValueError("Invalid flow decision in the text file")

        line = prev_file.readline().strip()
        flow = float(line)  # Read flow value from the previous file

        while flow < THRESHOLD and increasing:
            flow += random.uniform(*WATER_FLOW_RANGE)  # Increase water flow gradually
            water_flow_data.append(flow)
            if flow >= THRESHOLD:
                increasing = False  # Switch to decreasing once the threshold is reached
                decision_file.seek(0)  # Reset the file position to update the decision
                decision_file.write("decrease")  # Update the flow decision in the file
                decision_file.truncate()  # Clear any remaining content in the file

        while flow > 8 and not increasing:
            flow -= random.uniform(*WATER_FLOW_RANGE)  # Decrease water flow gradually
            if flow < 8:
                flow = 8
                increasing = True  # Switch to increasing once the minimum value is reached
                decision_file.seek(0)  # Reset the file position to update the decision
                decision_file.write("increase")  # Update the flow decision in the file
                decision_file.truncate()
            water_flow_data.append(flow)
            if flow <= 8:
                increasing = True  # Switch to increasing once the minimum value is reached
                decision_file.seek(0)  # Reset the file position to update the decision
                decision_file.write("increase")  # Update the flow decision in the file
                decision_file.truncate()  # Clear any remaining content in the file

    water_flow_data = water_flow_data[:NUM_ZONES]  # Truncate the list to the desired length
    return water_flow_data



# Function to generate random wastage detection
def detect_water_wastage(water_flow_data):
    return [flow > THRESHOLD for flow in water_flow_data]

# Function to play beep sound
def play_beep_sound():
    frequency = 2500  # Adjust the frequency as per your requirements
    duration = 1000  # Adjust the duration as per your requirements
    winsound.Beep(frequency, duration)

# Function to capture camera frame


# Streamlit application
def main():
    st.title("Irrigation Management System")

    while True:
        # Generate random sensor data
        moisture_data = generate_sensor_data()

        # Display moisture data
        st.subheader("Moisture Data")
        moisture_df = pd.DataFrame({"Zone": range(1, NUM_ZONES+1), "Moisture": moisture_data})
        st.dataframe(moisture_df)

        # Generate random water flow data
        water_flow_data = generate_water_flow_data()

        # Write water flow data to a text file
        with open("water_flow_data.txt", "w") as file:
            file.write("\n".join(str(flow) for flow in water_flow_data))

        # Display water flow data
        st.subheader("Water Flow Data")
        water_flow_df = pd.DataFrame({"Zone": range(1, NUM_ZONES+1), "Water Flow": water_flow_data})
        st.dataframe(water_flow_df)

        # Plot graphs
        st.subheader("Data Visualization")
        fig, axes = plt.subplots(2, 1, figsize=(8, 6))
        axes[0].bar(range(1, NUM_ZONES+1), moisture_data)
        axes[0].set_ylabel("Moisture (%)")
        axes[1].bar(range(1, NUM_ZONES+1), water_flow_data)
        axes[1].set_ylabel("Water Flow (liters/min)")
        st.pyplot(fig)

        # Water wastage detection
        st.subheader("Water Wastage Detection")
        wastage_detected = detect_water_wastage(water_flow_data)
        if any(wastage_detected):
            st.warning("Water wastage detected!")
            play_beep_sound()
            break
        # Camera integration
        

        # Wait for some time before updating again
        time.sleep(1) 
        st.experimental_rerun()
    st.header("irrigation status")
    st.success("Irrigation complete")

if __name__ == "__main__":
    main()
