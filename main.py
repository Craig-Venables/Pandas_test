import pandas as pd
import numpy
import os
import Data as eq
import matplotlib.pyplot as plt
import plot as plot
import file as f
from file import filepath

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


# Pull voltage and current data from file
v_data, c_data = eq.split_iv_sweep(filepath)
# get positive and negative vlaues of voltage and current data for equations later
v_data_ps, c_data_ps = eq.filter_positive_values(v_data, c_data)
v_data_ng, c_data_ng = eq.filter_negative_values(v_data, c_data)

num_sweeps = eq.check_for_loops(v_data)
eq.area_under_curves(v_data,c_data)

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

# print variable names for the folders and add too dataframe
for variable_name, folder_name in file_info.items():
    df[variable_name] = folder_name



#print(df)



if plot_graph:
    p = plot.plot(df, file_info)
    p.main_plot()
if save_df:
    # save the sada frame
    print(long_name)
    df.to_csv(long_name, index=False)
