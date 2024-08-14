import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the provided .txt file
# Assuming the .txt file is space-separated, you can change 'sep' if it's tab-separated or comma-separated
path = r"C:\Users\Craig-Desktop\OneDrive - The University of Nottingham\Documents\Phd\2) Data\1) Devices\1) Memristors\Quantum Dots\Zn-Cu-In-S(Zns)\D65-0.05mgml-ITO-PMMA(3%)-Gold-s5\G\10\44-fs-1.5v-0.05sv-100na-10sweeps-1mw-0.4v-edurance.txt"

# Load the data from the provided .txt file with the correct separator
data = pd.read_csv(path, sep="\t", header=0,
                   names=['Voltage', 'Current'])


# Assuming the data is collected in 20 cycles, we will divide the data accordingly
number_of_cycles = 10
rows_per_cycle = len(data) // number_of_cycles

# Create a 'Cycle' column by repeating cycle numbers for each set of rows
cycle_numbers = np.repeat(np.arange(number_of_cycles), rows_per_cycle)

# If there are remaining rows that don't fit evenly into the cycles, add them to the last cycle
if len(cycle_numbers) < len(data):
    cycle_numbers = np.append(cycle_numbers, [number_of_cycles - 1] * (len(data) - len(cycle_numbers)))

# Assign the cycle numbers to the data
data['Cycle'] = cycle_numbers

# Print the first few rows to confirm correct parsing
print("First few rows of the dataset with Cycle numbers added:")
print(data.head())

# Define the correct column names
cycle_column = 'Cycle'
voltage_column = 'Voltage'
current_column = 'Current'

# Define the voltages at which we want to calculate the ON/OFF ratios
voltages = [0.1, 0.15, 0.2]

# Initialize dictionaries to hold ON/OFF ratios for each voltage
on_off_ratios_positive = {v: [] for v in voltages}
on_off_ratios_negative = {v: [] for v in voltages}

# Get unique cycles
cycles = data[cycle_column].unique()

# Loop through each cycle (sweep)
for cycle in cycles:
    cycle_data = data[data[cycle_column] == cycle]

    for voltage in voltages:
        # Filter data for the specific voltage
        on_data = cycle_data[cycle_data[voltage_column] == voltage]
        off_data = cycle_data[cycle_data[voltage_column] == -voltage]

        # Calculate ON/OFF ratios
        if not on_data.empty and not off_data.empty:
            on_off_ratio_positive = on_data[current_column].max() / off_data[current_column].min()
            on_off_ratio_negative = off_data[current_column].max() / on_data[current_column].min()

            on_off_ratios_positive[voltage].append(on_off_ratio_positive)
            on_off_ratios_negative[voltage].append(on_off_ratio_negative)

# Convert the dictionaries to dataframes for easier plotting
on_off_ratios_df_positive = pd.DataFrame(on_off_ratios_positive)
on_off_ratios_df_negative = pd.DataFrame(on_off_ratios_negative)

# Save the ON/OFF ratios to a CSV file
#on_off_ratios_df_positive.to_csv('C:/Users/Craig-Desktop/on_off_ratios_positive.csv', index=False)
#on_off_ratios_df_negative.to_csv('C:/Users/Craig-Desktop/on_off_ratios_negative.csv', index=False)

# Plotting
for voltage in voltages:
    plt.figure(figsize=(10, 6))
    plt.plot(cycles, on_off_ratios_df_positive[voltage], label=f'Positive ON/OFF ratio at {voltage} V', marker='o')
    plt.plot(cycles, on_off_ratios_df_negative[voltage], label=f'Negative ON/OFF ratio at {voltage} V', marker='x')
    plt.xlabel('Cycle')
    plt.ylabel('ON/OFF Ratio')
    plt.title(f'ON/OFF Ratio vs Cycle for Voltage {voltage} V')
    plt.legend()

    # Check if all values are positive before applying log scale
    all_positive = np.all(on_off_ratios_df_positive[voltage] > 0) and np.all(on_off_ratios_df_negative[voltage] > 0)

    if all_positive:
        plt.yscale('log')
    else:
        print(f"Skipping log scale for voltage {voltage} V due to non-positive values.")

    plt.grid(True)
    plt.savefig(f'C:/Users/Craig-Desktop/on_off_ratio_{voltage}V.png')
    plt.show()