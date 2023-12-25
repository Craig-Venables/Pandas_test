import pandas as pd
import numpy
import os
import Data as eq
import matplotlib.pyplot as plt
import plot as plot
import file as f
from file import filepath,excell_path
import excell as ex

# to add
# Todo add in the device name and polymer etc into the graphs when they get saved
# Todo Statistics - add section that counts the number of sweeps each device has completed
                 #- pull data from the statisitcs sheet i fill out when measuring the devices
                 #- histogram all the data
                 #- reorganise the functions
#
# Add a try except when file reading, so if the first way dosnt work it tries something else.
# i.e tries csv or a different method of extracting data from a text file
# add something about working out what kind of data i am taking and it should react acodingly

save_df = False
plot_graph = True
eq.set_pandas_display_options()
file_info = f.extract_folder_names(filepath)
short_name = f.short_name()
long_name = f.long_name()

print ("Currently working on -", file_info.get('file_name'))
print ('Information on file below:')
for variable_name, folder_name in file_info.items():
    print(f"{variable_name} = '{folder_name}'")

# what type of data is this?
# check how many columns it has and match it against something that tells you what data
# ie Iv sweeps = 2 columns named voltage and current

# Pull voltage and current data from file
v_data, c_data = eq.split_iv_sweep(filepath)
# get positive and negative vlaues of voltage and current data for equations later
v_data_ps, c_data_ps = eq.filter_positive_values(v_data, c_data)
v_data_ng, c_data_ng = eq.filter_negative_values(v_data, c_data)
# checks for looped data and calculates the number of loops
num_sweeps = eq.check_for_loops(v_data)

# if there is more than one loop adds
if num_sweeps > 1:
    # Data processing for multiple sweeps
    print("There are ", num_sweeps, " loops within this data")

    # splits the loops  depending on the number of sweeps
    split_v_data, split_c_data = eq.split_loops(v_data,c_data,num_sweeps)
    # Calculates the metrics for each array returning the areas
    ps_areas, ng_areas, areas, normalized_areas = eq.calculate_metrics_for_loops(split_v_data,split_c_data)

    # Analyze the array changes
    percent_change, avg_change,avg_relative_change, std_relative_change = eq.analyze_array_changes(normalized_areas)

    print(f"Percentage change over the length: {percent_change:.5f}%")
    print(f"Average change over time: {avg_change:.2e}")
    print(f"Average relative change: {avg_relative_change:.5e}")
    print(f"Standard deviation of relative change: {std_relative_change:.5e}")

    # Plot the array values on a logarithmic scale
    plt.plot(normalized_areas, marker='o', linestyle='-')
    plt.yscale('log')
    plt.xlabel('Index')
    plt.ylabel('Value (log scale)')
    plt.title('Array Values on Logarithmic Scale')
    plt.grid(True)
    plt.show()

    def plot_array_changes(arr):
        # Create a range for the x-axis (indices of the array)
        x = range(len(arr))

        # Plot the array values
        plt.plot(x, arr, marker='o', linestyle='-')

        # Set labels and title
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Change of Values in the Array')

        # Show the plot
        plt.show()
    #plots the changes over time for each array and the loops.
    #plot_array_changes(normalized_areas)

else:
    # Data Processing for a single sweep
    print("data contains only one sweep")

    ps_area_enclosed, ng_area_enclosed, area_enclosed, norm_area_enclosed = eq.area_under_curves(v_data, c_data)
    print("total area enclosed within the hysteresis normalised to voltage = ", norm_area_enclosed)
    # this area will need passing back too a another array for comparision across all devices in the section



# create dataframe for device
data = {'voltage': v_data,
        'current': c_data,
        'abs_current': eq.absolute_val(c_data),
        'resistance': eq.resistance(v_data, c_data),
        'voltage_ps': v_data_ps,
        'current_ps': c_data_ps,
        'voltage_ng': v_data_ng,
        'current_ng': c_data_ng,
        'log_Resistance': eq.log_value(eq.resistance(v_data, c_data)),
        'abs_Current_ps': eq.absolute_val(c_data_ps),
        'abs_Current_ng': eq.absolute_val(c_data_ng),
        'current_Density_ps': eq.current_density_eq(v_data_ps, c_data_ps),
        'current_Density_ng': eq.current_density_eq(v_data_ng, c_data_ng),
        'electric_field_ps': eq.electric_field_eq(v_data_ps),
        'electric_field_ng': eq.electric_field_eq(v_data_ng),
        'inverse_resistance_ps': eq.inverse_resistance_eq(v_data_ps, c_data_ps),
        'inverse_resistance_ng': eq.inverse_resistance_eq(v_data_ng, c_data_ng),
        'sqrt_Voltage': eq.sqrt_array(v_data),
        'on_off_ratio': eq.statistics}





df = pd.DataFrame(data)

# print variable names dd too dataframe
for variable_name, folder_name in file_info.items():
    df[variable_name] = folder_name


# Get information
#ex.save_info(file_info.get('sample_name'),excell_path,savelocation)


if plot_graph:
    p = plot.plot(df, file_info)
    p.main_plot()
if save_df:
    # save the sada frame
    print(long_name)
    df.to_csv(long_name, index=False)
