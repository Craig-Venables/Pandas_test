import pandas as pd
import numpy
import os
import Data as eq
import matplotlib.pyplot as plt
import plot as plot
import file as f
from file import filepath, excell_path
import excell as ex

# to add
# Statistics
# - add a section that counts the number of sweeps each device has completed
# - pull data from the statistics sheet i fill out when measuring the devices
# - histogram all the data
# - for sweeps what's the internal area of each sweep and how does it compare to the previous?
#   list these in a table for printing after and the amount they have reduced from the previous and
#   the first value in percentage?


save_df = False
plot_graph = True
eq.set_pandas_display_options()
file_info = f.extract_folder_names(filepath)
short_name = f.short_name()
long_name = f.long_name()

print("Currently working on -", file_info.get('file_name'))
print('Information on file below:')
for variable_name, folder_name in file_info.items():
    print(f"{variable_name} = '{folder_name}'")

# Pull voltage and current data from file
v_data, c_data = eq.split_iv_sweep(filepath)
# get positive and negative vlaues of voltage and current data for equations later
v_data_ps, c_data_ps = eq.filter_positive_values(v_data, c_data)
v_data_ng, c_data_ng = eq.filter_negative_values(v_data, c_data)

num_sweeps = eq.check_for_loops(v_data)
ps_area_enclosed, ng_area_enclosed, total_area_enclosed = eq.area_under_curves(v_data, c_data)
# print("Area enclosed by the curve ps = ",ps_area_enclosed)
# print("Area enclosed by the curve ng = ", ng_area_enclosed)
print("total area enclosed within the hysteresis = ", total_area_enclosed)
# todo normalise this area acroding to voltage as curerently it preferences higher voltages as they give a larger area.

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

# todo find a way to call the dataframe the name of the file and then save it appropratly
# add in the device name and polymer etc into the graphs when they get saved


df = pd.DataFrame(data)

# print variable names dd too dataframe
for variable_name, folder_name in file_info.items():
    df[variable_name] = folder_name

# Get information
# ex.save_info(file_info.get('sample_name'),excell_path,savelocation)
print("short name", short_name)

# print(df)


if plot_graph:
    p = plot.plot(df, file_info)
    p.main_plot()
if save_df:
    # save the sada frame
    print(long_name)
    df.to_csv(long_name, index=False)
